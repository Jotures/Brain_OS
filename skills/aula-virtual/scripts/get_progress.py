#!/usr/bin/env python3
"""
Tracker de Progreso de Actividades — Brain OS
===============================================
Muestra el progreso de completado de actividades por curso,
usando el sistema de tracking de Moodle (completion tracking).

Usage:
    python get_progress.py                          # Todos los cursos
    python get_progress.py --course "Economía"      # Filtrar por curso
    python get_progress.py --brief                  # Resumen compacto
    python get_progress.py --json                   # Output JSON
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Cargar entorno
try:
    from dotenv import load_dotenv
    skill_dir = Path(__file__).parent.parent
    env_path = skill_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

from moodle_api import MoodleAPI, MoodleAPIError
from course_map import COURSE_MAP, find_brain_os_course


def make_progress_bar(percentage: float, width: int = 20) -> str:
    """Genera una barra de progreso visual."""
    filled = int(width * percentage / 100)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {percentage:.0f}%"


def get_all_progress(api: MoodleAPI, course_filter: str = None) -> List[Dict]:
    """
    Obtiene el progreso de todos los cursos mapeados.
    
    Args:
        api: Instancia de MoodleAPI
        course_filter: String parcial para filtrar por nombre de curso
    
    Returns:
        Lista de dicts con progreso por curso
    """
    courses = api.get_courses()
    results = []
    
    for course in courses:
        moodle_name = course['fullname']
        course_info = find_brain_os_course(moodle_name)
        
        if not course_info:
            continue
        
        # Filtrar si se especificó
        if course_filter:
            filter_lower = course_filter.lower()
            name_lower = course_info['name'].lower()
            if filter_lower not in name_lower and name_lower not in filter_lower:
                continue
        
        course_id = course['id']
        
        try:
            summary = api.get_course_progress_summary(course_id)
        except Exception:
            summary = {'total': 0, 'completed': 0, 'pending': 0, 'percentage': 0, 'activities': []}
        
        results.append({
            'brain_os_id': course_info['id'],
            'name': course_info['name'],
            'emoji': course_info['emoji'],
            'moodle_id': course_id,
            **summary,
        })
    
    return results


def format_full_report(progress_data: List[Dict]) -> str:
    """Genera reporte completo de progreso."""
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("📊 PROGRESO DE ACTIVIDADES — Brain OS")
    lines.append(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("=" * 60)
    
    for course in progress_data:
        emoji = course['emoji']
        name = course['name']
        total = course['total']
        done = course['completed']
        pct = course['percentage']
        
        lines.append(f"\n{emoji} {name}")
        
        if total == 0:
            lines.append("   ⬜ Sin actividades con tracking habilitado")
            continue
        
        bar = make_progress_bar(pct)
        lines.append(f"   {bar} ({done}/{total} actividades)")
        
        # Listar actividades pendientes (agrupadas por sección)
        pending = [a for a in course.get('activities', []) if not a['completed']]
        
        if pending:
            sections = {}
            for act in pending:
                sec = act.get('section', 'General')
                sections.setdefault(sec, []).append(act)
            
            lines.append(f"   📋 Pendientes ({len(pending)}):")
            for section_name, acts in sections.items():
                if section_name:
                    lines.append(f"      📁 {section_name}:")
                for act in acts:
                    type_emoji = _get_type_emoji(act.get('activity_type', ''))
                    lines.append(f"         {type_emoji} {act['name']}")
        else:
            lines.append("   ✅ ¡Todas las actividades completadas!")
    
    lines.append("\n" + "=" * 60)
    
    # Resumen global
    total_all = sum(c['total'] for c in progress_data)
    done_all = sum(c['completed'] for c in progress_data)
    pct_all = round((done_all / total_all) * 100, 1) if total_all > 0 else 0
    
    lines.append(f"\n🎯 Progreso global: {make_progress_bar(pct_all)} ({done_all}/{total_all})")
    
    return "\n".join(lines)


def format_brief(progress_data: List[Dict]) -> str:
    """Genera resumen compacto (para boot matutino)."""
    lines = ["📊 Progreso rápido:"]
    
    for course in progress_data:
        emoji = course['emoji']
        name = course['name'][:25]
        total = course['total']
        done = course['completed']
        pct = course['percentage']
        
        if total == 0:
            lines.append(f"  {emoji} {name}: —")
        else:
            bar_mini = "█" * int(5 * pct / 100) + "░" * (5 - int(5 * pct / 100))
            lines.append(f"  {emoji} {name}: [{bar_mini}] {pct:.0f}% ({done}/{total})")
    
    return "\n".join(lines)


def _get_type_emoji(modname: str) -> str:
    """Retorna emoji según tipo de actividad Moodle."""
    emojis = {
        'assign': '📝',
        'quiz': '❓',
        'forum': '💬',
        'resource': '📄',
        'url': '🔗',
        'page': '📃',
        'folder': '📁',
        'label': '🏷️',
        'choice': '🗳️',
        'feedback': '📋',
        'workshop': '🔧',
        'lesson': '📖',
        'glossary': '📚',
        'wiki': '📝',
        'data': '🗃️',
    }
    return emojis.get(modname, '▫️')


def main():
    parser = argparse.ArgumentParser(description='Tracker de progreso de actividades Moodle')
    parser.add_argument('--course', type=str, help='Filtrar por nombre de curso')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--brief', action='store_true', help='Resumen compacto')
    args = parser.parse_args()
    
    try:
        api = MoodleAPI()
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    if not args.json:
        print("⏳ Consultando progreso de actividades...", file=sys.stderr)
    
    progress = get_all_progress(api, course_filter=args.course)
    
    if args.json:
        # Limpiar actividades para JSON
        output = []
        for p in progress:
            clean = {k: v for k, v in p.items()}
            output.append(clean)
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.brief:
        print(format_brief(progress))
    else:
        print(format_full_report(progress))


if __name__ == "__main__":
    main()
