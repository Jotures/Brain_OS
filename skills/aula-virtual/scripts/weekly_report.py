#!/usr/bin/env python3
"""
Reporte Semanal de Rendimiento — Brain OS
==========================================
Genera un reporte semanal que combina:
- Notas actuales por curso (gradebook)
- Progreso de actividades
- Tareas completadas vs pendientes
- Tendencias comparadas con la semana anterior

Mantiene un histórico en data/weekly_history.json.

Usage:
    python weekly_report.py               # Generar reporte
    python weekly_report.py --save        # Guardar snapshot + reporte
    python weekly_report.py --json        # Output JSON del snapshot
    python weekly_report.py --history     # Ver historial de snapshots
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
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
from get_grades import get_all_grades
from get_progress import get_all_progress

# Historial persistente
HISTORY_FILE = Path(__file__).parent / "data" / "weekly_history.json"

# Ruta al historial de Pomodoro
POMODORO_HISTORY = Path(__file__).parent.parent.parent / "tools" / "pomodoro" / "history.json"


def load_history() -> Dict:
    """Carga el histórico de snapshots semanales."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"weeks": []}


def save_history(history: Dict) -> None:
    """Guarda el histórico."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def get_pomodoro_count_this_week() -> int:
    """Lee el conteo de pomodoros de esta semana desde el historial del timer."""
    if not POMODORO_HISTORY.exists():
        return 0
    
    try:
        with open(POMODORO_HISTORY, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Calcular inicio de la semana (lunes)
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        count = 0
        for session in data.get('sessions', []):
            session_date_str = session.get('date', '')
            if session_date_str:
                try:
                    session_date = datetime.fromisoformat(session_date_str).date()
                    if session_date >= week_start:
                        count += 1
                except ValueError:
                    pass
        
        return count
    except (json.JSONDecodeError, IOError):
        return 0


def generate_snapshot(api: MoodleAPI) -> Dict:
    """
    Genera un snapshot del rendimiento actual.
    
    Returns:
        Dict con toda la data de la semana
    """
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    # 1. Notas actuales
    grades = get_all_grades(api)
    grades_snapshot = {}
    for g in grades:
        if not g.get('error') and g['average'] is not None:
            grades_snapshot[g['brain_os_id']] = {
                'average': g['average'],
                'graded_count': g.get('graded_count', 0),
            }
    
    # 2. Progreso de actividades
    progress = get_all_progress(api)
    progress_snapshot = {}
    for p in progress:
        progress_snapshot[p['brain_os_id']] = {
            'total': p['total'],
            'completed': p['completed'],
            'percentage': p['percentage'],
        }
    
    # 3. Pomodoros de esta semana
    pomodoro_count = get_pomodoro_count_this_week()
    
    return {
        'week_start': str(week_start),
        'generated_at': datetime.now().isoformat(),
        'grades': grades_snapshot,
        'progress': progress_snapshot,
        'pomodoro_count': pomodoro_count,
    }


def calculate_trends(current: Dict, previous: Optional[Dict]) -> Dict:
    """
    Compara snapshot actual vs. anterior para generar tendencias.
    
    Returns:
        Dict con tendencias por curso
    """
    if not previous:
        return {}
    
    trends = {}
    
    # Tendencias de notas
    for course_id, current_data in current.get('grades', {}).items():
        prev_data = previous.get('grades', {}).get(course_id)
        if prev_data:
            diff = current_data['average'] - prev_data['average']
            if diff > 0.5:
                trend = '↑'
            elif diff < -0.5:
                trend = '↓'
            else:
                trend = '→'
            trends[course_id] = {
                'grade_trend': trend,
                'grade_diff': round(diff, 2),
            }
    
    # Tendencias de progreso
    for course_id, current_data in current.get('progress', {}).items():
        prev_data = previous.get('progress', {}).get(course_id)
        if prev_data:
            diff = current_data['completed'] - prev_data['completed']
            if course_id not in trends:
                trends[course_id] = {}
            trends[course_id]['activities_diff'] = diff
    
    return trends


def format_report(snapshot: Dict, trends: Dict, history: Dict) -> str:
    """Genera reporte semanal en texto formateado."""
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append("📈 REPORTE SEMANAL DE RENDIMIENTO — Brain OS")
    lines.append(f"📅 Semana del {snapshot['week_start']}")
    lines.append(f"🕐 Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("=" * 60)
    
    # Sección 1: Notas
    lines.append("\n📊 CALIFICACIONES")
    lines.append("-" * 40)
    
    alerts = []
    for course_id, grade_data in snapshot.get('grades', {}).items():
        course_info = COURSE_MAP.get(course_id, {})
        emoji = course_info.get('emoji', '📌')
        name = course_info.get('name', course_id)
        avg = grade_data['average']
        
        # Trend indicator
        trend_info = trends.get(course_id, {})
        trend_str = trend_info.get('grade_trend', '')
        diff = trend_info.get('grade_diff', 0)
        trend_display = f" {trend_str} ({diff:+.1f})" if trend_str else ""
        
        status = "🔴" if avg < NOTA_MINIMA_APROBATORIA else "✅"
        lines.append(f"  {emoji} {name}: {avg:.1f}/20 {status}{trend_display}")
        
        if avg < NOTA_MINIMA_APROBATORIA:
            alerts.append(f"⚠️ {name}: nota {avg:.1f} bajo mínimo ({NOTA_MINIMA_APROBATORIA})")
    
    if not snapshot.get('grades'):
        lines.append("  Sin notas registradas aún.")
    
    # Sección 2: Progreso
    lines.append("\n📋 PROGRESO DE ACTIVIDADES")
    lines.append("-" * 40)
    
    total_all = 0
    done_all = 0
    for course_id, prog_data in snapshot.get('progress', {}).items():
        course_info = COURSE_MAP.get(course_id, {})
        emoji = course_info.get('emoji', '📌')
        name = course_info.get('name', course_id)[:25]
        total = prog_data['total']
        done = prog_data['completed']
        pct = prog_data['percentage']
        total_all += total
        done_all += done
        
        # Activities diff
        trend_info = trends.get(course_id, {})
        act_diff = trend_info.get('activities_diff', 0)
        act_str = f" (+{act_diff} esta semana)" if act_diff > 0 else ""
        
        filled = int(10 * pct / 100)
        bar = "█" * filled + "░" * (10 - filled)
        lines.append(f"  {emoji} {name}: [{bar}] {pct:.0f}% ({done}/{total}){act_str}")
    
    if not snapshot.get('progress'):
        lines.append("  Sin datos de progreso.")
    
    # Sección 3: Productividad
    lines.append("\n🍅 PRODUCTIVIDAD")
    lines.append("-" * 40)
    pomodoros = snapshot.get('pomodoro_count', 0)
    lines.append(f"  Pomodoros esta semana: {pomodoros}")
    
    if total_all > 0:
        global_pct = round((done_all / total_all) * 100, 1)
        lines.append(f"  Progreso global: {global_pct}% ({done_all}/{total_all} actividades)")
    
    # Alertas
    if alerts:
        lines.append("\n⚠️  ALERTAS")
        lines.append("-" * 40)
        for alert in alerts:
            lines.append(f"  {alert}")
    
    # Historial
    weeks_count = len(history.get('weeks', []))
    lines.append(f"\n📚 Historial: {weeks_count} semanas registradas")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Reporte semanal de rendimiento académico')
    parser.add_argument('--save', action='store_true', help='Guardar snapshot en histórico')
    parser.add_argument('--json', action='store_true', help='Output JSON del snapshot')
    parser.add_argument('--history', action='store_true', help='Ver historial de snapshots')
    args = parser.parse_args()
    
    # Modo historia
    if args.history:
        history = load_history()
        weeks = history.get('weeks', [])
        if not weeks:
            print("📚 No hay snapshots guardados aún.")
            print("   Usa --save para guardar el primer snapshot.")
        else:
            print(f"📚 Historial ({len(weeks)} semanas):\n")
            for w in weeks[-5:]:  # Últimas 5
                print(f"  📅 Semana {w['week_start']} — Generado: {w.get('generated_at', '?')[:10]}")
                grades = w.get('grades', {})
                for cid, g in grades.items():
                    name = COURSE_MAP.get(cid, {}).get('name', cid)[:20]
                    print(f"     {name}: {g['average']:.1f}")
        return
    
    try:
        api = MoodleAPI()
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    if not args.json:
        print("⏳ Generando reporte semanal...", file=sys.stderr)
    
    # Generar snapshot
    snapshot = generate_snapshot(api)
    
    if args.json:
        print(json.dumps(snapshot, indent=2, ensure_ascii=False))
        return
    
    # Cargar historial y calcular tendencias
    history = load_history()
    previous = history['weeks'][-1] if history['weeks'] else None
    trends = calculate_trends(snapshot, previous)
    
    # Guardar si se pidió
    if args.save:
        history['weeks'].append(snapshot)
        save_history(history)
        print("💾 Snapshot guardado.", file=sys.stderr)
    
    # Mostrar reporte
    print(format_report(snapshot, trends, history))


if __name__ == "__main__":
    main()
