#!/usr/bin/env python3
"""
Sync Assignments + Calendar Events: Moodle -> Notion (BD_TAREAS_MAESTRAS)
=========================================================================
Fetches assignments and calendar events from Moodle and creates/updates them in Notion.
Now with intelligent auto-priority based on gradebook weight + deadline proximity.

Fixes aplicados:
  - FIX #1: duedate == 0 ya no genera fecha 1/1/1970 en Notion
  - FIX #2: HEADERS se construye en tiempo de ejecución (no en importación),
            evitando "Bearer None" cuando .env carga después del import
  - FIX #3: Prioridad calculada automáticamente según días restantes
"""

import os
import requests
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Cargar .env ANTES de cualquier otra cosa
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

from moodle_api import MoodleAPI
from course_map import COURSE_MAP, find_brain_os_course, NOTION_DB_TAREAS, NOTION_DB_AREAS, MOODLE_URL
from get_tasks import calculate_urgency, get_assignment_weight


# =============================================================================
# FIX #2: Headers construidos en función, no en tiempo de importación
# =============================================================================

def get_notion_headers() -> dict:
    """
    Construye los headers de Notion en tiempo de ejecución.
    Garantiza que NOTION_TOKEN ya esté cargado desde .env.
    """
    token = os.getenv('NOTION_TOKEN')
    if not token:
        raise ValueError(
            "NOTION_TOKEN no encontrado. "
            "Agrega NOTION_TOKEN=... a skills/aula-virtual/.env"
        )
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }


DATABASE_ID = NOTION_DB_TAREAS


# =============================================================================
# FIX #3: Cálculo de Prioridad
# =============================================================================
def calculate_priority(duedate_ts: int) -> str:
    """
    Calcula la prioridad según días restantes hasta el deadline.
      <= 3 días  → 🔥 Alta
      <= 7 días  → ⚡ Media
      >  7 días  → ☁️ Baja
      sin fecha  → ⚡ Media (valor por defecto)
    """
    if not duedate_ts or duedate_ts == 0:
        return "⚡ Media"

    now = datetime.now(timezone.utc).timestamp()
    days_remaining = (duedate_ts - now) / 86400

    if days_remaining <= 3:
        return "🔥 Alta"
    elif days_remaining <= 7:
        return "⚡ Media"
    else:
        return "☁️ Baja"


# =============================================================================
# Mapeo de Cursos desde Notion (BD_AREAS)
# =============================================================================
def get_course_mapping() -> dict:
    """
    Retorna un diccionario {notion_page_id: nombre_curso} de BD_AREAS.
    """
    headers = get_notion_headers()
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_AREAS}/query"
    has_more = True
    next_cursor = None
    mapping = {}

    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor

        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for page in data.get("results", []):
            page_id = page["id"]
            props = page.get("properties", {})
            title_prop = props.get("Nombre", {}).get("title", [])
            if title_prop:
                name = title_prop[0]["plain_text"]
                mapping[page_id] = name

        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")

    return mapping

def find_course_notion_id(moodle_name: str, mapping: dict) -> str | None:
    """
    Busca el notion_id del curso usando course_map.py como fuente de verdad.
    Primero intenta match por patrones de course_map, luego fallback a fuzzy.
    """
    # Método 1: usar find_brain_os_course (fuente de verdad del ecosistema)
    course_info = find_brain_os_course(moodle_name)
    if course_info:
        notion_id = course_info.get("notion_id")
        if notion_id:
            return notion_id

    # Método 2: fuzzy match contra nombres en Notion (fallback)
    def normalize(s: str) -> str:
        return (s.lower()
                .replace('á','a').replace('é','e').replace('í','i')
                .replace('ó','o').replace('ú','u').replace('ñ','n'))

    m_norm = normalize(moodle_name)
    for nid, nname in mapping.items():
        if normalize(nname) in m_norm or m_norm in normalize(nname):
            return nid

    return None


# =============================================================================
# Verificación de duplicados en Notion
# =============================================================================
def task_exists_in_notion(name: str) -> tuple[bool, str | None, dict | None]:
    """
    Verifica si una tarea ya existe en BD_TAREAS_MAESTRAS por título exacto.
    Retorna (existe, page_id, properties).
    """
    headers = get_notion_headers()
    query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Tarea",
            "title": {"equals": name}
        }
    }
    resp = requests.post(query_url, headers=headers, json=payload, timeout=30)
    results = resp.json().get('results', [])

    if results:
        return True, results[0]['id'], results[0]['properties']
    return False, None, None


# =============================================================================
# Sincronización principal
# =============================================================================
def sync_assignments(preview: bool = False):
    mode_label = "[PREVIEW] " if preview else ""
    print(f"🚀 {mode_label}Starting Assignment Sync...")

    api = MoodleAPI()

    # 0. Cargar mapeo de cursos desde Notion
    print("   🗺️  Loading Notion Course Mapping...")
    course_map = get_course_mapping()
    print(f"      Mapped {len(course_map)} courses from Notion.")

    # 1. Obtener tareas desde Moodle
    print("   📥 Fetching assignments from Moodle...")
    data = api.get_assignments()

    created_count = 0
    skipped_count = 0
    repaired_count = 0

    for course in data.get('courses', []):
        course_name = course.get('fullname', '')
        course_id = course.get('id')
        assignments = course.get('assignments', [])

        if not assignments:
            continue

        print(f"\n📚 Course: {course_name}")

        # Buscar notion_id del curso
        notion_course_id = find_course_notion_id(course_name, course_map)

        if not notion_course_id:
            print(f"   ⚠️  No se encontró curso en Notion. Se creará sin relación.")
        else:
            linked_name = course_map.get(notion_course_id, notion_course_id)
            print(f"      ✅ Linked to: {linked_name}")

        for assign in assignments:
            name = assign.get('name', 'Sin nombre')
            duedate = assign.get('duedate', 0)  # 0 = sin fecha límite en Moodle
            cmid = assign.get('cmid')

            # ── FIX #3: Calcular prioridad ──────────────────────────────────
            # Se usa la lógica de calculate_priority pero HEAD tenía una más avanzada
            # Integramos la avanzada de HEAD
            
            due_date_iso = None
            due_date_display = "Sin fecha"
            if duedate and duedate > 0:
                dt = datetime.fromtimestamp(duedate, tz=timezone.utc)
                due_date_iso = dt.strftime("%Y-%m-%d")
                due_date_display = dt.strftime("%d/%m/%Y")

            # ── Verificar duplicado ─────────────────────────────────────────
            exists, page_id, existing_props = task_exists_in_notion(name)

            if exists:
                # Reparar relación faltante si corresponde
                current_relation = existing_props.get("Área/Curso", {}).get("relation", [])
                if not current_relation and notion_course_id:
                    print(f"   🔧 Repairing missing relation for: {name}")
                    if not preview:
                        headers = get_notion_headers()
                        requests.patch(
                            f"https://api.notion.com/v1/pages/{page_id}",
                            headers=headers,
                            json={"properties": {"Área/Curso": {"relation": [{"id": notion_course_id}]}}},
                            timeout=30
                        )
                    repaired_count += 1
                else:
                    print(f"   ⏭️  Exists (skip): {name}")
                    skipped_count += 1
                continue

            # ── Crear Pág en Notion ─────────────────────────────────────────
            if preview:
                print(f"   📝 [PREVIEW] Se crearía: '{name}' | {due_date_display}")
                created_count += 1
                continue

            # Calcular prioridad inteligente (v2.2 logic)
            import time as _time
            current_ts = _time.time()
            days_remaining = int((duedate - current_ts) / (24 * 60 * 60)) if duedate else 30
            weight_info = get_assignment_weight(api, course_id, name)
            _, auto_priority = calculate_urgency(days_remaining, weight_info['weight'])

            print(f"   ✨ Creating: '{name}' | {due_date_display} | {auto_priority}")

            properties = {
                "Tarea": {
                    "title": [{"text": {"content": name}}]
                },
                "Tipo": {
                    "select": {"name": "📝 Tarea"}
                },
                "Estado": {
                    "status": {"name": "Por hacer"}
                },
                "Prioridad": {
                    "select": {"name": auto_priority}
                },
                "Aporte": {
                    "select": {"name": "Aporte 1"}
                }
            }

            # FIX #1: Solo añadir Fecha Entrega si hay fecha válida
            if due_date_iso:
                properties["Fecha Entrega"] = {
                    "date": {"start": due_date_iso}
                }

            # Relación con curso
            if notion_course_id:
                properties["Área/Curso"] = {
                    "relation": [{"id": notion_course_id}]
                }

            # Blocks de contenido: link a Moodle
            moodle_link = f"{MOODLE_URL}/mod/assign/view.php?id={cmid}" if cmid else MOODLE_URL
            children_blocks = [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {"type": "text", "text": {"content": "Ir a Moodle: "}},
                            {"type": "text", "text": {
                                "content": "Abrir Tarea",
                                "link": {"url": moodle_link}
                            }}
                        ],
                        "icon": {"emoji": "🎓"},
                        "color": "gray_background"
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {
                            "content": "Sincronizado automáticamente desde Moodle."
                        }}]
                    }
                }
            ]

            new_page = {
                "parent": {"database_id": DATABASE_ID},
                "properties": properties,
                "children": children_blocks,
            }

            headers = get_notion_headers()
            create_resp = requests.post(
                "https://api.notion.com/v1/pages",
                headers=headers,
                json=new_page,
                timeout=30
            )

            if create_resp.status_code == 200:
                print("      ✅ Created.")
                created_count += 1
            else:
                print(f"      ❌ Error: {create_resp.text[:200]}")

    # Resumen
    print(f"\n{'='*55}")
    print(f"🏁 Sync Complete.")
    print(f"   ✅ {created_count} tasks {'would be ' if preview else ''}created")
    print(f"   ⏭️  {skipped_count} tasks skipped (already exist)")
    print(f"   🔧 {repaired_count} relations repaired")
    print(f"{'='*55}")



def sync_calendar_events(preview: bool = False):
    """Sincroniza eventos del calendario de Moodle (quizzes, exámenes) a Notion."""
    mode_label = "[PREVIEW] " if preview else ""
    print(f"\n📅 {mode_label}Syncing Calendar Events...")
    
    api = MoodleAPI()
    events = api.get_upcoming_events(days=30)
    
    # Filtrar solo eventos que NO son assignments (ya los cubre sync_assignments)
    non_assign_events = [e for e in events if e['module_name'] != 'assign']
    
    if not non_assign_events:
        print("   ℹ️ No calendar events found beyond assignments.")
        return
    
    print(f"   Found {len(non_assign_events)} calendar events.")
    
    # Cargar course mapping de Notion
    course_map_notion = get_course_mapping()
    created = 0
    
    for event in non_assign_events:
        name = event['name']
        event_type = event['type']  # '⚡ Examen' o '📅 Evento'
        
        # Verificar si ya existe en Notion
        query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        payload = {
            "filter": {
                "property": "Tarea",
                "title": {"equals": name}
            }
        }
        headers = get_notion_headers()
        resp = requests.post(query_url, headers=headers, json=payload)
        existing = resp.json().get('results', [])
        
        if existing:
            print(f"   ⏭️ Exists (skip): {name}")
            continue
        
        if preview:
            print(f"   📅 [PREVIEW] Se crearía: {event_type} — {name} ({event['timestart_formatted']})")
            created += 1
            continue
        
        # Buscar relación con curso en Notion
        notion_course_id = None
        if event.get('course_name'):
            notion_course_id = find_course_notion_id(event['course_name'], course_map_notion)
        
        # Calcular prioridad
        days_rem = event.get('days_remaining', 30)
        _, auto_priority = calculate_urgency(days_rem, weight=None)
        
        # Crear en Notion
        print(f"   ✨ Creating: {event_type} — {name}")
        new_page = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Tarea": {
                    "title": [{"text": {"content": name}}]
                },
                "Fecha Entrega": {
                    "date": {"start": datetime.fromtimestamp(event['timestart']).isoformat()}
                },
                "Tipo": {
                    "select": {"name": event_type}
                },
                "Estado": {
                    "status": {"name": "Por hacer"}
                },
                "Prioridad": {
                    "select": {"name": auto_priority}
                },
                "Aporte": {
                    "select": {"name": "Aporte 1"}
                }
            }
        }
        
        if notion_course_id:
            new_page["properties"]["Área/Curso"] = {
                "relation": [{"id": notion_course_id}]
            }
        
        # Añadir link al evento si disponible
        event_url = event.get('url', '')
        if event_url:
            new_page["children"] = [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {"type": "text", "text": {"content": "Ir a Moodle: "}},
                            {"type": "text", "text": {"content": "Abrir Evento", "link": {"url": event_url}}}
                        ],
                        "icon": {"emoji": "📅"},
                        "color": "gray_background"
                    }
                }
            ]
        
        create_resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=new_page)
        if create_resp.status_code == 200:
            print("      ✅ Created.")
            created += 1
        else:
            print(f"      ❌ Error: {create_resp.text}")
    
    print(f"\n📅 Calendar Sync Complete. Created {created} events.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sync Moodle assignments + calendar to Notion')
    parser.add_argument('--preview', action='store_true', help='Preview sin crear en Notion')
    parser.add_argument('--no-calendar', action='store_true', help='Skip calendar sync')
    args = parser.parse_args()
    
    sync_assignments(preview=args.preview)
    
    if not args.no_calendar:
        sync_calendar_events(preview=args.preview)
