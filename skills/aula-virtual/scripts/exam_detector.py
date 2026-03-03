#!/usr/bin/env python3
"""
Detector de Exámenes — Brain OS
=================================
Detecta exámenes, quizzes y evaluaciones próximas usando el
calendario de Moodle. Alimenta al pre_exam_orchestrator.

Usage:
    python exam_detector.py                     # Listar próximos exámenes
    python exam_detector.py --days 14           # Ventana de 14 días
    python exam_detector.py --course "Operativa" # Filtrar por curso
    python exam_detector.py --json              # Output JSON
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

# Patrones que indican examen/evaluación
EXAM_KEYWORDS = [
    'examen', 'exam', 'quiz', 'cuestionario', 'evaluación', 'evaluacion',
    'parcial', 'final', 'práctica calificada', 'practica calificada',
    'control', 'test', 'prueba',
]


def detect_upcoming_exams(
    api: MoodleAPI,
    days_threshold: int = 7,
    course_filter: str = None
) -> List[Dict]:
    """
    Detecta exámenes y evaluaciones próximas en Moodle.
    
    Combina dos fuentes:
    1. Calendario de eventos (quizzes, eventos de curso)
    2. Assignments con nombres que indican evaluación
    
    Args:
        api: Instancia de MoodleAPI
        days_threshold: Días hacia adelante para buscar
        course_filter: Filtrar por nombre parcial de curso
    
    Returns:
        Lista de exámenes detectados ordenados por fecha
    """
    exams = []
    seen_names = set()
    
    # Fuente 1: Eventos del calendario
    events = api.get_upcoming_events(days=days_threshold)
    for event in events:
        name_lower = event['name'].lower()
        is_exam = (
            event.get('module_name') == 'quiz'
            or any(kw in name_lower for kw in EXAM_KEYWORDS)
        )
        
        if not is_exam:
            continue
        
        # Filtrar por curso si se pide
        if course_filter:
            course_name = event.get('course_name', '')
            course_info = find_brain_os_course(course_name) if course_name else None
            brain_os_name = course_info['name'] if course_info else course_name
            if course_filter.lower() not in brain_os_name.lower():
                continue
        
        # Enriquecer con info de Brain OS
        course_name = event.get('course_name', '')
        course_info = find_brain_os_course(course_name)
        
        exam_key = f"{event['name']}_{event.get('course_id', '')}"
        if exam_key in seen_names:
            continue
        seen_names.add(exam_key)
        
        exams.append({
            'name': event['name'],
            'course_name': course_info['name'] if course_info else course_name,
            'course_id': course_info['id'] if course_info else None,
            'emoji': course_info['emoji'] if course_info else '📌',
            'date': event['timestart_formatted'],
            'timestamp': event['timestart'],
            'days_until': event['days_remaining'],
            'source': 'calendar',
            'module_type': event.get('module_name', ''),
            'url': event.get('url', ''),
            'notebooklm_url': course_info.get('notebooklm_url', '') if course_info else '',
        })
    
    # Fuente 2: Assignments con nombre de examen
    try:
        assignments = api.get_assignments()
        import time
        now = int(time.time())
        future = now + (days_threshold * 24 * 60 * 60)
        
        for course in assignments.get('courses', []):
            course_name = course.get('fullname', '')
            course_info = find_brain_os_course(course_name)
            
            if course_filter and course_info:
                if course_filter.lower() not in course_info['name'].lower():
                    continue
            
            for assign in course.get('assignments', []):
                due_date = assign.get('duedate', 0)
                if not (now < due_date <= future):
                    continue
                
                name_lower = assign.get('name', '').lower()
                is_exam = any(kw in name_lower for kw in EXAM_KEYWORDS)
                
                if not is_exam:
                    continue
                
                exam_key = f"{assign['name']}_{course.get('id', '')}"
                if exam_key in seen_names:
                    continue
                seen_names.add(exam_key)
                
                days_until = (due_date - now) // (24 * 60 * 60)
                
                exams.append({
                    'name': assign['name'],
                    'course_name': course_info['name'] if course_info else course_name,
                    'course_id': course_info['id'] if course_info else None,
                    'emoji': course_info['emoji'] if course_info else '📌',
                    'date': datetime.fromtimestamp(due_date).strftime('%Y-%m-%d %H:%M'),
                    'timestamp': due_date,
                    'days_until': days_until,
                    'source': 'assignment',
                    'module_type': 'assign',
                    'url': f"https://campus.uandina.edu.pe/mod/assign/view.php?id={assign.get('cmid', '')}",
                    'notebooklm_url': course_info.get('notebooklm_url', '') if course_info else '',
                })
    except MoodleAPIError:
        pass
    
    # Ordenar por fecha
    exams.sort(key=lambda x: x['timestamp'])
    return exams


def check_exam_proximity(api: MoodleAPI, topic: str, days: int = 7) -> Dict:
    """
    Verifica si un tema/curso tiene un examen próximo.
    
    Args:
        api: Instancia de MoodleAPI
        topic: Nombre del tema o curso
        days: Ventana de días
    
    Returns:
        Dict con has_exam (bool) + datos del examen si existe
    """
    exams = detect_upcoming_exams(api, days_threshold=days, course_filter=topic)
    
    if exams:
        return {
            'has_exam': True,
            'exam_count': len(exams),
            'nearest_exam': exams[0],
            'all_exams': exams,
        }
    
    return {'has_exam': False, 'exam_count': 0}


def main():
    parser = argparse.ArgumentParser(description='Detector de exámenes próximos')
    parser.add_argument('--days', type=int, default=14, help='Ventana de búsqueda en días')
    parser.add_argument('--course', type=str, help='Filtrar por curso')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    args = parser.parse_args()
    
    try:
        api = MoodleAPI()
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    if not args.json:
        print("🔍 Detectando exámenes próximos...", file=sys.stderr)
    
    exams = detect_upcoming_exams(api, days_threshold=args.days, course_filter=args.course)
    
    if args.json:
        print(json.dumps(exams, indent=2, ensure_ascii=False))
        return
    
    print("")
    print("=" * 55)
    print("📝 EXÁMENES Y EVALUACIONES PRÓXIMAS")
    print(f"📅 Ventana: próximos {args.days} días")
    print("=" * 55)
    
    if not exams:
        print("\n✅ No se detectaron exámenes próximos.")
        return
    
    for exam in exams:
        days = exam['days_until']
        
        # Urgencia visual
        if days <= 2:
            urgency = "🔴 URGENTE"
        elif days <= 5:
            urgency = "🟠 PRONTO"
        else:
            urgency = "🟡 PREPARAR"
        
        print(f"\n{exam['emoji']} {exam['course_name']}")
        print(f"   📝 {exam['name']}")
        print(f"   📅 {exam['date']} ({days}d) — {urgency}")
        print(f"   🔗 {exam['url']}" if exam['url'] else "")
    
    print(f"\n📊 Total: {len(exams)} evaluaciones detectadas")


if __name__ == "__main__":
    main()
