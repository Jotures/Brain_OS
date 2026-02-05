#!/usr/bin/env python3
"""
Sync Tasks to Notion
====================
Sincroniza tareas del Aula Virtual UAndina a BD_TAREAS_MAESTRAS en Notion.

Usage:
    python sync_to_notion.py           # Sincroniza tareas pendientes
    python sync_to_notion.py --preview # Preview sin crear en Notion
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Añadir el directorio de scripts al path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from get_tasks import get_pending_tasks
from course_map import find_brain_os_course, NOTION_DB_TAREAS

# Cargar entorno
try:
    from dotenv import load_dotenv
    skill_dir = script_dir.parent
    env_path = skill_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def format_task_for_notion(task: dict) -> dict:
    """
    Formatea una tarea de Moodle para crear en Notion.
    
    Args:
        task: Diccionario con datos de la tarea de Moodle
        
    Returns:
        Diccionario con propiedades para Notion API
    """
    # Buscar el curso correspondiente en Brain OS
    course_info = find_brain_os_course(task['course'])
    
    # Determinar prioridad según días restantes
    days = task.get('days_remaining', 30)
    if days <= 2:
        priority = "🔴 Urgente"
    elif days <= 7:
        priority = "🟡 Alta"
    else:
        priority = "🟢 Normal"
    
    # Formatear fecha para Notion (ISO 8601)
    due_date = datetime.fromtimestamp(task['due_date']).strftime('%Y-%m-%d')
    
    notion_task = {
        'name': task['name'],
        'due_date': due_date,
        'priority': priority,
        'source': 'Aula Virtual',
        'moodle_link': task.get('link', ''),
        'moodle_id': task.get('assignment_id'),
        'course_moodle': task['course'],
    }
    
    if course_info:
        notion_task['course_brain_os'] = course_info['name']
        notion_task['course_emoji'] = course_info['emoji']
        notion_task['course_notion_id'] = course_info['notion_id']
    else:
        notion_task['course_brain_os'] = 'Otro'
        notion_task['course_emoji'] = '📚'
        notion_task['course_notion_id'] = None
    
    return notion_task


def create_notion_task(task: dict) -> dict:
    """
    Crea una tarea en Notion usando la MCP API.
    
    Args:
        task: Tarea formateada para Notion
        
    Returns:
        Respuesta de Notion o error
    """
    # Nota: Esta función será llamada por el agente usando MCP
    # Por ahora retornamos el formato para que el agente pueda crear
    return {
        'parent': {'database_id': NOTION_DB_TAREAS},
        'properties': {
            'Nombre': {
                'title': [{'text': {'content': task['name']}}]
            },
            'Fecha límite': {
                'date': {'start': task['due_date']}
            },
            'Prioridad': {
                'select': {'name': task['priority']}
            },
            'Origen': {
                'select': {'name': 'Aula Virtual'}
            },
            'Curso': {
                'select': {'name': task['course_brain_os']}
            },
            'Link': {
                'url': task['moodle_link'] if task['moodle_link'] else None
            }
        }
    }


def sync_tasks_to_notion(preview: bool = False) -> List[Dict]:
    """
    Sincroniza todas las tareas pendientes a Notion.
    
    Args:
        preview: Si True, solo muestra qué se crearía sin crear
        
    Returns:
        Lista de tareas procesadas
    """
    print("🔄 Sincronizando tareas del Aula Virtual a Notion...")
    print("=" * 50)
    
    # Obtener tareas pendientes
    tasks = get_pending_tasks()
    
    if not tasks:
        print("✅ No hay tareas pendientes para sincronizar.")
        return []
    
    print(f"📋 Encontradas {len(tasks)} tareas pendientes\n")
    
    results = []
    
    for task in tasks:
        notion_task = format_task_for_notion(task)
        
        # Mostrar info
        emoji = notion_task['course_emoji']
        name = notion_task['name'][:40]
        course = notion_task['course_brain_os']
        priority = notion_task['priority']
        due = notion_task['due_date']
        
        print(f"{emoji} {name}...")
        print(f"   📖 {course}")
        print(f"   📅 {due} | {priority}")
        
        if preview:
            print(f"   📝 [PREVIEW] Se crearía en Notion")
        else:
            # Aquí el agente usaría MCP para crear en Notion
            notion_payload = create_notion_task(notion_task)
            print(f"   📤 Listo para crear en Notion")
            results.append({
                'task': notion_task,
                'notion_payload': notion_payload
            })
        
        print()
    
    print("=" * 50)
    if preview:
        print(f"📋 Preview completado: {len(tasks)} tareas")
    else:
        print(f"✅ Sincronización preparada: {len(results)} tareas listas")
        print("\n💡 El agente puede ahora crear estas tareas en Notion usando MCP")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Sync tasks to Notion')
    parser.add_argument('--preview', action='store_true', 
                       help='Preview without creating in Notion')
    args = parser.parse_args()
    
    results = sync_tasks_to_notion(preview=args.preview)
    
    # Si hay resultados y no es preview, guardar para uso del agente
    if results and not args.preview:
        output_path = script_dir.parent / "data" / "pending_sync.json"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Payload guardado en: {output_path}")


if __name__ == "__main__":
    main()
