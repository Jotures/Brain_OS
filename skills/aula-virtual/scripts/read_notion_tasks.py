#!/usr/bin/env python3
"""
Read Tasks from Notion
======================
Lee tareas pendientes de BD_TAREAS_MAESTRAS en Notion.

Parte de la integración bidireccional Brain OS ↔ Notion.
Este script es llamado automáticamente cuando el usuario pregunta
por tareas pendientes.

Usage:
    python read_notion_tasks.py           # Todas las tareas pendientes
    python read_notion_tasks.py --curso X # Filtrar por curso
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# ID de la base de datos BD_TAREAS_MAESTRAS (verificado)
NOTION_DB_TAREAS = "2cbaacd6-8210-803b-b9d9-d78fa3066b2a"


def get_urgency_indicator(due_date_str: Optional[str]) -> str:
    """Retorna emoji de urgencia según la fecha límite."""
    if not due_date_str:
        return "⚪"  # Sin fecha
    
    try:
        due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        now = datetime.now(due_date.tzinfo) if due_date.tzinfo else datetime.now()
        days_remaining = (due_date - now).days
        
        if days_remaining < 0:
            return "⚫"  # Vencida
        elif days_remaining <= 2:
            return "🔴"  # Urgente
        elif days_remaining <= 7:
            return "🟡"  # Pronto
        else:
            return "🟢"  # Normal
    except:
        return "⚪"


def format_task_for_display(task: dict) -> dict:
    """Formatea una tarea de Notion para mostrar."""
    props = task.get('properties', {})
    
    # Extraer nombre
    name = "Sin título"
    if 'Nombre' in props and props['Nombre'].get('title'):
        name = props['Nombre']['title'][0]['plain_text']
    elif 'Name' in props and props['Name'].get('title'):
        name = props['Name']['title'][0]['plain_text']
    
    # Extraer fecha
    due_date = None
    for date_field in ['Fecha límite', 'Fecha', 'Due', 'Date']:
        if date_field in props and props[date_field].get('date'):
            due_date = props[date_field]['date'].get('start')
            break
    
    # Extraer curso
    course = "General"
    for course_field in ['Curso', 'Área', 'Area']:
        if course_field in props and props[course_field].get('select'):
            course = props[course_field]['select']['name']
            break
    
    # Extraer origen
    origin = "Manual"
    if 'Origen' in props and props['Origen'].get('select'):
        origin = props['Origen']['select']['name']
    
    return {
        'id': task['id'],
        'name': name,
        'due_date': due_date,
        'course': course,
        'origin': origin,
        'urgency': get_urgency_indicator(due_date),
        'url': task.get('url', '')
    }


def display_tasks(tasks: List[dict], title: str = "Tareas de Notion"):
    """Muestra las tareas de forma visual."""
    print(f"\n📋 {title}")
    print("=" * 50)
    
    if not tasks:
        print("✅ No hay tareas pendientes en Notion")
        return
    
    # Agrupar por urgencia
    urgent = [t for t in tasks if t['urgency'] == '🔴']
    soon = [t for t in tasks if t['urgency'] == '🟡']
    normal = [t for t in tasks if t['urgency'] == '🟢']
    other = [t for t in tasks if t['urgency'] in ['⚪', '⚫']]
    
    for group, label in [(urgent, "URGENTE"), (soon, "PRONTO"), (normal, "NORMAL"), (other, "OTRAS")]:
        if group:
            print(f"\n{group[0]['urgency']} {label}:")
            for task in group:
                origin_tag = f"[{task['origin']}]" if task['origin'] != 'Manual' else ""
                date_str = task['due_date'][:10] if task['due_date'] else "Sin fecha"
                print(f"   • {task['name'][:40]}")
                print(f"     📖 {task['course']} | 📅 {date_str} {origin_tag}")
    
    print("\n" + "=" * 50)
    print(f"Total: {len(tasks)} tareas pendientes")


def main():
    """
    Punto de entrada principal.
    
    NOTA: Este script está diseñado para ser ejecutado por el agente
    usando la herramienta MCP de Notion. Las queries reales se hacen
    a través de mcp_notion-mcp-server_API-query-data-source.
    """
    print("📋 Brain OS - Lector de Tareas Notion")
    print("=" * 50)
    print()
    print("Este script es ejecutado por el agente AI.")
    print("Para ver tus tareas, di:")
    print()
    print('  "¿Qué tareas tengo?"')
    print('  "Tareas de Economía Ambiental"')
    print('  "Mis pendientes de esta semana"')
    print()
    print(f"📊 BD_TAREAS_MAESTRAS: {NOTION_DB_TAREAS[:8]}...")


if __name__ == "__main__":
    main()
