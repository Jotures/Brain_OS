#!/usr/bin/env python3
"""
Dashboard de Calificaciones — Brain OS
=======================================
Consulta el gradebook de Moodle y muestra un dashboard con:
- Nota actual de cada curso
- Promedio ponderado
- Alertas si alguna nota está bajo el mínimo aprobatorio
- Desglose por items evaluados

Usage:
    python get_grades.py              # Dashboard visual
    python get_grades.py --json       # Output JSON estructurado
    python get_grades.py --brief      # Resumen compacto (para boot matutino)
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
from course_map import COURSE_MAP, find_brain_os_course, NOTA_MINIMA_APROBATORIA


def get_all_grades(api: MoodleAPI) -> List[Dict]:
    """
    Obtiene las calificaciones de todos los cursos mapeados en Brain OS.
    
    Returns:
        Lista de dicts con info de curso + calificaciones
    """
    courses = api.get_courses()
    results = []
    
    for course in courses:
        moodle_name = course['fullname']
        course_info = find_brain_os_course(moodle_name)
        
        if not course_info:
            continue
        
        course_id = course['id']
        
        try:
            grades_data = api.get_grades(course_id)
        except MoodleAPIError:
            results.append({
                'brain_os_id': course_info['id'],
                'name': course_info['name'],
                'emoji': course_info['emoji'],
                'moodle_id': course_id,
                'error': True,
                'items': [],
                'average': None,
            })
            continue
        
        # Procesar grade items
        items = []
        total_weighted_grade = 0.0
        total_max = 0.0
        graded_count = 0
        
        for table in grades_data.get('usergrades', []):
            for item in table.get('gradeitems', []):
                item_name = item.get('itemname')
                if not item_name:
                    continue
                
                grade_raw = item.get('graderaw')
                grade_max = item.get('grademax', 20)
                percentage = item.get('percentageformatted', '-')
                
                # Limpiar porcentaje
                pct_value = None
                if percentage and percentage != '-':
                    try:
                        pct_value = float(percentage.replace('%', '').replace(',', '.').strip())
                    except ValueError:
                        pass
                
                item_data = {
                    'name': item_name,
                    'grade': grade_raw,
                    'max_grade': grade_max,
                    'percentage': pct_value,
                    'percentage_str': percentage,
                    'feedback': item.get('feedback', ''),
                }
                items.append(item_data)
                
                # Acumular para promedio (solo ítems calificados)
                if grade_raw is not None and grade_max and grade_max > 0:
                    total_weighted_grade += grade_raw
                    total_max += grade_max
                    graded_count += 1
        
        # Calcular promedio normalizado a escala vigesimal
        average = None
        if total_max > 0:
            average = round((total_weighted_grade / total_max) * 20, 2)
        
        results.append({
            'brain_os_id': course_info['id'],
            'name': course_info['name'],
            'emoji': course_info['emoji'],
            'moodle_id': course_id,
            'error': False,
            'items': items,
            'graded_count': graded_count,
            'average': average,
            'below_minimum': average is not None and average < NOTA_MINIMA_APROBATORIA,
        })
    
    return results


def format_dashboard(grades: List[Dict]) -> str:
    """Genera un dashboard visual de calificaciones."""
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("🎓 DASHBOARD DE CALIFICACIONES — Brain OS")
    lines.append(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("=" * 60)
    
    alerts = []
    
    for course in grades:
        emoji = course['emoji']
        name = course['name']
        avg = course['average']
        
        if course.get('error'):
            lines.append(f"\n{emoji} {name}: ❌ Error al consultar")
            continue
        
        # Indicador de estado
        if avg is None:
            status = "⬜ Sin notas"
            avg_str = "—"
        elif course['below_minimum']:
            status = "🔴 BAJO MÍNIMO"
            avg_str = f"{avg:.1f}/20"
            alerts.append(f"⚠️ {name}: {avg_str} (mínimo: {NOTA_MINIMA_APROBATORIA})")
        elif avg >= 16:
            status = "🟢 Excelente"
            avg_str = f"{avg:.1f}/20"
        elif avg >= 14:
            status = "🔵 Bueno"
            avg_str = f"{avg:.1f}/20"
        else:
            status = "🟡 Regular"
            avg_str = f"{avg:.1f}/20"
        
        graded = course.get('graded_count', 0)
        lines.append(f"\n{emoji} {name}")
        lines.append(f"   Promedio: {avg_str}  {status}")
        lines.append(f"   Evaluaciones calificadas: {graded}")
        
        # Mostrar items calificados
        for item in course['items']:
            grade = item['grade']
            max_g = item['max_grade']
            if grade is not None:
                pct = item['percentage_str']
                lines.append(f"   ├─ {item['name']}: {grade:.1f}/{max_g:.0f} ({pct})")
            else:
                lines.append(f"   ├─ {item['name']}: Sin calificar")
    
    lines.append("\n" + "=" * 60)
    
    # Alertas
    if alerts:
        lines.append("\n⚠️  ALERTAS:")
        for alert in alerts:
            lines.append(f"   {alert}")
    else:
        lines.append("\n✅ Todas las notas sobre el mínimo aprobatorio.")
    
    lines.append(f"\n📌 Mínimo aprobatorio: {NOTA_MINIMA_APROBATORIA}/20")
    
    return "\n".join(lines)


def format_brief(grades: List[Dict]) -> str:
    """Genera resumen compacto de una línea por curso (para boot matutino)."""
    lines = ["📊 Notas rápidas:"]
    
    for course in grades:
        avg = course['average']
        emoji = course['emoji']
        name = course['name'][:25]
        
        if course.get('error'):
            lines.append(f"  {emoji} {name}: ❌")
        elif avg is None:
            lines.append(f"  {emoji} {name}: —")
        elif course['below_minimum']:
            lines.append(f"  {emoji} {name}: {avg:.1f} 🔴")
        else:
            lines.append(f"  {emoji} {name}: {avg:.1f} ✅")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Dashboard de calificaciones Moodle')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--brief', action='store_true', help='Resumen compacto')
    args = parser.parse_args()
    
    try:
        api = MoodleAPI()
    except ValueError as e:
        print(f"❌ {e}")
        print("   Ejecuta: python get_uandina_token.py")
        return
    
    print("⏳ Consultando calificaciones..." if not args.json else "", file=sys.stderr)
    
    grades = get_all_grades(api)
    
    if args.json:
        # Limpiar para JSON serializable
        output = []
        for g in grades:
            clean = {k: v for k, v in g.items()}
            output.append(clean)
        print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.brief:
        print(format_brief(grades))
    else:
        print(format_dashboard(grades))


if __name__ == "__main__":
    main()
