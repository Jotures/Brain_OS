#!/usr/bin/env python3
"""
Sync Assignments + Calendar Events: Moodle -> Notion (BD_TAREAS_MAESTRAS)
=========================================================================
Fetches assignments and calendar events from Moodle and creates/updates them in Notion.
Now with intelligent auto-priority based on gradebook weight + deadline proximity.
"""

import os
import json
import argparse
import requests
from datetime import datetime
from moodle_api import MoodleAPI
from course_map import COURSE_MAP, find_brain_os_course, NOTION_DB_TAREAS, NOTION_DB_AREAS, MOODLE_URL
from get_tasks import calculate_urgency, get_assignment_weight

# Setup
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = NOTION_DB_TAREAS
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_course_mapping():
    """
    Retorna un diccionario {course_id: course_name} de la base de datos de Cursos.
    """
    url = f"https://api.notion.com/v1/databases/{NOTION_DB_AREAS}/query"
    has_more = True
    next_cursor = None
    mapping = {}

    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor

        resp = requests.post(url, headers=HEADERS, json=payload)
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

def find_course_id_by_name(moodle_name, mapping):
    # Mapping is {notion_id: notion_name}
    # We need to find the notion_id where notion_name matches moodle_name loosely
    
    # Normalization helper
    def normalize(s):
        return s.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')

    m_norm = normalize(moodle_name)
    
    # Specific overrides if normalization isn't enough
    if "investigacion operativa" in m_norm: return next((k for k,v in mapping.items() if "investigacion operativa" in normalize(v)), None)
    if "investigacion economica" in m_norm: return next((k for k,v in mapping.items() if "investigacion economica" in normalize(v)), None)
    if "teoria monetaria" in m_norm: return next((k for k,v in mapping.items() if "teoria monetaria" in normalize(v)), None)
    if "economia y gestion publica" in m_norm: return next((k for k,v in mapping.items() if "gestion publica" in normalize(v)), None)
    if "economia internacional" in m_norm: return next((k for k,v in mapping.items() if "economia internacional" in normalize(v)), None)

    # General search
    for nid, nname in mapping.items():
        if normalize(nname) in m_norm or m_norm in normalize(nname):
            return nid
            
    return None



def sync_assignments(preview: bool = False):
    mode_label = "[PREVIEW] " if preview else ""
    print(f"🚀 {mode_label}Starting Assignment Sync...")
    api = MoodleAPI()
    
    # 0. Get Course Mapping
    print("   🗺️ Loading Notion Course Mapping...")
    course_map = get_course_mapping()
    print(f"      Mapped {len(course_map)} courses from Notion.")

    # 1. Get Assignments
    print("   📥 Fetching assignments from Moodle...")
    data = api.get_assignments()
    
    # 2. Iterate
    msg_count = 0
    
    for course in data.get('courses', []):
        course_name = course.get('fullname')
        course_id = course.get('id')
        assignments = course.get('assignments', [])
        
        if not assignments:
            continue
            
        print(f"\n📚 Course: {course_name}")
        
        # Find Notion Course ID using robust mapping
        notion_course_id = find_course_id_by_name(course_name, course_map)
        
        if not notion_course_id:
            print(f"   ⚠️ Could not link to Notion Course. Skipping relation.")
        else:
            print(f"      ✅ Linked to: {course_map[notion_course_id]}")
        
        for assign in assignments:
            name = assign.get('name')

            due_date = assign.get('duedate')
            intro = assign.get('intro', '') # Warning: HTML
            assign_id = assign.get('id')
            
            # Skip if due date is passed long ago? (Optional)
            # For now, sync all.
            
            # Check if exists in Notion
            # Criteria: Title = Name AND Course = Relation? Or just Title?
            # Let's search by Title first.
            query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
            payload = {
                "filter": {
                    "property": "Tarea",
                    "title": {
                        "equals": name
                    }
                }
            }
            resp = requests.post(query_url, headers=HEADERS, json=payload)
            existing = resp.json().get('results', [])
            
            if existing:
                page_id = existing[0]['id']
                existing_props = existing[0]['properties']
                
                # Check if relation is missing
                # "Área/Curso": { "relation": [...] }
                current_relation = existing_props.get("Área/Curso", {}).get("relation", [])
                
                if not current_relation and notion_course_id:
                    print(f"   🔧 Repairing missing relation for: {name}")
                    update_url = f"https://api.notion.com/v1/pages/{page_id}"
                    update_payload = {
                        "properties": {
                            "Área/Curso": {
                                "relation": [{"id": notion_course_id}]
                            }
                        }
                    }
                    requests.patch(update_url, headers=HEADERS, json=update_payload)
                else:
                    print(f"   ⏭️ Exists (skip): {name}")
                
                continue
            
            # Preview mode: solo mostrar, no crear
            if preview:
                due_str = datetime.fromtimestamp(due_date).strftime('%d/%m/%Y') if due_date else 'Sin fecha'
                print(f"   📝 [PREVIEW] Se crearía: {name} (vence: {due_str})")
                msg_count += 1
                continue

            # Create
            # Calcular prioridad inteligente
            import time as _time
            current_ts = _time.time()
            days_remaining = int((due_date - current_ts) / (24 * 60 * 60)) if due_date else 30
            weight_info = get_assignment_weight(api, course_id, name)
            _, auto_priority = calculate_urgency(days_remaining, weight_info['weight'])
            
            print(f"   ✨ Creating: {name} (Priority: {auto_priority})")
            new_page = {
                "parent": {"database_id": DATABASE_ID},
                "properties": {
                    "Tarea": {
                        "title": [{"text": {"content": name}}]
                    },
                    "Fecha Entrega": {
                        "date": {"start": datetime.fromtimestamp(due_date).isoformat()}
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
            }
            
            if notion_course_id:
                new_page["properties"]["Área/Curso"] = {
                    "relation": [{"id": notion_course_id}]
                }
            
            # Add Link to Moodle
            # Construction: .../mod/assign/view.php?id={cmid} -> wait, assign['cmid'] ? or is it id?
            # API returns 'cmid' usually or we can construct from 'id' ?
            # 'id' in response is assignment instance id. 'cmid' is course module id.
            # get_assignments returns 'cmid' usually.
            cmid = assign.get('cmid')
            moodle_link = f"{MOODLE_URL}/mod/assign/view.php?id={cmid}"
            
            # Add to content
            children_blocks = [
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {"type": "text", "text": {"content": "Ir a Moodle: "}},
                            {"type": "text", "text": {"content": "Abrir Tarea", "link": {"url": moodle_link}}}
                        ],
                        "icon": {"emoji": "🎓"},
                        "color": "gray_background"
                    }
                },
                {
                     "object": "block",
                     "type": "paragraph",
                     "paragraph": {
                         "rich_text": [{"type": "text", "text": {"content": "Sincronizado automáticamente desde Moodle."}}]
                     }
                }
            ]
            
            new_page["children"] = children_blocks

            
            create_resp = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=new_page)
            if create_resp.status_code == 200:
                print("      ✅ Created.")
                msg_count += 1
            else:
                print(f"      ❌ Error: {create_resp.text}")

    print(f"\n🏁 Sync Complete. Created {msg_count} tasks.")


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
        resp = requests.post(query_url, headers=HEADERS, json=payload)
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
            notion_course_id = find_course_id_by_name(event['course_name'], course_map_notion)
        
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
        
        create_resp = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=new_page)
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
