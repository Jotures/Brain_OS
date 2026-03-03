#!/usr/bin/env python3
"""
Orquestador Pre-Examen — Brain OS
====================================
Genera un payload de configuración inteligente para sesiones de estudio
pre-examen, conectando:
- Moodle (detección de exámenes)
- Pomodoro (perfil exam_prep)
- NotebookLM (URL del notebook del curso)

NO modifica las skills directamente — genera config JSON que el agente
LLM interpreta para orquestar las sesiones.

Usage:
    python pre_exam_orchestrator.py --course "Operativa"   # Generar config
    python pre_exam_orchestrator.py --all                  # Todos los cursos con examen
    python pre_exam_orchestrator.py --json                 # Output sólo JSON
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
from course_map import COURSE_MAP
from exam_detector import detect_upcoming_exams, check_exam_proximity


# Mapeo de intensidad según días restantes
INTENSITY_MAP = {
    1: {'profile': 'exam_prep', 'questions': 7, 'intensity': 'critical', 'bloom': ['evaluate', 'create']},
    2: {'profile': 'exam_prep', 'questions': 6, 'intensity': 'high', 'bloom': ['analyze', 'evaluate']},
    3: {'profile': 'exam_prep', 'questions': 5, 'intensity': 'high', 'bloom': ['apply', 'analyze']},
    5: {'profile': 'intensive', 'questions': 4, 'intensity': 'medium', 'bloom': ['apply', 'analyze']},
    7: {'profile': 'intensive', 'questions': 3, 'intensity': 'medium', 'bloom': ['understand', 'apply']},
}


def get_intensity_config(days_until: int) -> Dict:
    """Determina la configuración de intensidad según días al examen."""
    for threshold, config in sorted(INTENSITY_MAP.items()):
        if days_until <= threshold:
            return config
    # Default para >7 días
    return {'profile': 'default', 'questions': 3, 'intensity': 'low', 'bloom': ['remember', 'understand']}


def generate_pre_exam_config(exam: Dict) -> Dict:
    """
    Genera un payload de configuración pre-examen para un examen específico.
    
    Args:
        exam: Dict de examen (del exam_detector)
    
    Returns:
        Dict con configuración para Pomodoro + Active Recall + NotebookLM
    """
    days = exam['days_until']
    intensity = get_intensity_config(days)
    
    course_id = exam.get('course_id')
    course_info = COURSE_MAP.get(course_id, {}) if course_id else {}
    
    return {
        'exam': {
            'name': exam['name'],
            'course': exam['course_name'],
            'date': exam['date'],
            'days_remaining': days,
            'url': exam.get('url', ''),
        },
        'pomodoro': {
            'profile': intensity['profile'],
            'work_duration': {
                'exam_prep': 45,
                'intensive': 50,
                'default': 25,
            }.get(intensity['profile'], 25),
            'break_duration': {
                'exam_prep': 8,
                'intensive': 10,
                'default': 5,
            }.get(intensity['profile'], 5),
            'command': f"python pomodoro_timer.py start --topic \"{exam['course_name']}\" --mode {intensity['profile']}",
        },
        'active_recall': {
            'intensity': intensity['intensity'],
            'questions_per_session': intensity['questions'],
            'bloom_levels': intensity['bloom'],
            'strategy': _get_study_strategy(days),
        },
        'notebooklm': {
            'url': exam.get('notebooklm_url', course_info.get('notebooklm_url', '')),
            'action': 'Consultar temas clave del examen',
        },
        'recommendations': _get_recommendations(days, exam['course_name']),
    }


def _get_study_strategy(days_until: int) -> str:
    """Retorna estrategia de estudio según tiempo disponible."""
    if days_until <= 1:
        return "Repaso rápido: flashcards + preguntas de exámenes anteriores. No estudiar material nuevo."
    elif days_until <= 3:
        return "Práctica activa: resolver problemas tipo examen, Active Recall intensivo, resumir en voz alta."
    elif days_until <= 5:
        return "Consolidación: repasar apuntes, hacer esquemas, practicar ejercicios del sílabo."
    else:
        return "Preparación temprana: leer material, organizar apuntes, identificar temas débiles."


def _get_recommendations(days_until: int, course_name: str) -> List[str]:
    """Genera recomendaciones contextuales."""
    recs = []
    
    if days_until <= 2:
        recs.append("🔴 Prioriza SOLO este curso hoy")
        recs.append("🧠 Usa NotebookLM para generar preguntas de práctica")
        recs.append("😴 Duerme bien esta noche — el sueño consolida la memoria")
    elif days_until <= 5:
        recs.append("📋 Identifica los 3 temas más probables del examen")
        recs.append("📝 Haz un resumen de una página por tema")
        recs.append(f"🍅 Dedica al menos 2 sesiones Pomodoro diarias a {course_name}")
    else:
        recs.append("📚 Comienza revisando el sílabo y los objetivos del curso")
        recs.append("🔍 Consulta NotebookLM para identificar gaps de conocimiento")
        recs.append("📅 Planifica sesiones de estudio hasta el día del examen")
    
    return recs


def activate_pre_exam_mode(api: MoodleAPI, course_name: str) -> Optional[Dict]:
    """
    Punto de entrada principal: activa modo pre-examen para un curso.
    
    Returns:
        Config payload o None si no hay examen próximo
    """
    result = check_exam_proximity(api, course_name, days=14)
    
    if not result['has_exam']:
        return None
    
    return generate_pre_exam_config(result['nearest_exam'])


def main():
    parser = argparse.ArgumentParser(description='Orquestador de modo pre-examen')
    parser.add_argument('--course', type=str, help='Curso a preparar')
    parser.add_argument('--all', action='store_true', help='Todos los cursos con examen')
    parser.add_argument('--json', action='store_true', help='Output JSON puro')
    parser.add_argument('--days', type=int, default=14, help='Ventana de búsqueda')
    args = parser.parse_args()
    
    try:
        api = MoodleAPI()
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    if args.course:
        config = activate_pre_exam_mode(api, args.course)
        
        if args.json:
            print(json.dumps(config, indent=2, ensure_ascii=False) if config else '{"status": "no_exam"}')
            return
        
        if not config:
            print(f"\n✅ No se detectaron exámenes próximos para '{args.course}'.")
            return
        
        _print_config(config)
        return
    
    # Modo --all: buscar todos los exámenes
    exams = detect_upcoming_exams(api, days_threshold=args.days)
    
    if not exams:
        print("\n✅ No hay exámenes próximos detectados." if not args.json else '[]')
        return
    
    configs = [generate_pre_exam_config(e) for e in exams]
    
    if args.json:
        print(json.dumps(configs, indent=2, ensure_ascii=False))
        return
    
    print("")
    print("=" * 60)
    print("🎯 MODO PRE-EXAMEN — Configuraciones Generadas")
    print("=" * 60)
    
    for config in configs:
        _print_config(config)
        print("")


def _print_config(config: Dict):
    """Imprime una configuración de forma legible."""
    exam = config['exam']
    pomodoro = config['pomodoro']
    recall = config['active_recall']
    
    print(f"\n📝 Examen: {exam['name']}")
    print(f"   📖 Curso: {exam['course']}")
    print(f"   📅 Fecha: {exam['date']} ({exam['days_remaining']}d)")
    
    print(f"\n   🍅 Pomodoro:")
    print(f"      Perfil: {pomodoro['profile']} ({pomodoro['work_duration']}min/{pomodoro['break_duration']}min)")
    print(f"      Comando: {pomodoro['command']}")
    
    print(f"\n   🧠 Active Recall:")
    print(f"      Intensidad: {recall['intensity']}")
    print(f"      Preguntas/sesión: {recall['questions_per_session']}")
    print(f"      Niveles Bloom: {', '.join(recall['bloom_levels'])}")
    print(f"      Estrategia: {recall['strategy']}")
    
    nlm = config.get('notebooklm', {})
    if nlm.get('url'):
        print(f"\n   📓 NotebookLM: {nlm['url']}")
    
    recs = config.get('recommendations', [])
    if recs:
        print(f"\n   💡 Recomendaciones:")
        for rec in recs:
            print(f"      {rec}")


if __name__ == "__main__":
    main()
