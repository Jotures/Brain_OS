#!/usr/bin/env python3
"""
📊 Risk Score — Brain OS 2.2 (Fase 3)
======================================
Calcula semanalmente los 5 indicadores de alerta temprana de riesgo académico
a partir de los logs de sesiones Pomodoro.

Indicadores:
  1. Tasa de abandono      — Pomodoros abortados / iniciados        (> 20% → 🔴)
  2. Velocidad de consolidación — Gists score>7 / Pomodoro completado (< 0.5 → 🟡)
  3. Ratio Modo Crisis      — Pomodoros en crisis / total            (> 60% → 🔴)
  4. Execution Gap          — Planificados - Ejecutados              (> 3 → 🟡)
  5. Recovery Decay         — Tiempo de descanso promedio            (> 15 min → 🟡)

Fuentes de datos:
  - tools/pomodoro/history.json  (sesiones completadas)
  - config/semantic_memory.json  (gists con scores para consolidación)

Usage:
    python risk_score.py                # Reporte formateado para "Resume semana"
    python risk_score.py --json         # Output JSON para integración programática
    python risk_score.py --period week  # Período: today | week | month (default: week)
"""

import argparse
import io
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Forzar UTF-8 en stdout para Windows (emojis en cp1252 fallan)
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ─── Rutas ───────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent                             # skills/pomodoro/
BRAIN_OS_DIR = SKILL_DIR.parent.parent                    # Brain_OS/
POMODORO_HISTORY = BRAIN_OS_DIR / "tools" / "pomodoro" / "history.json"
SEMANTIC_MEMORY = BRAIN_OS_DIR / "config" / "semantic_memory.json"

# ─── Umbrales (del implementation_plan.md) ───────────────────────────
THRESHOLDS = {
    "abandonment_rate":       {"yellow": 0.10, "red": 0.20},
    "consolidation_velocity": {"yellow": 0.50, "red": 0.25},  # inverted: below is bad
    "crisis_ratio":           {"yellow": 0.40, "red": 0.60},
    "execution_gap":          {"yellow": 2,    "red": 3},
    "recovery_decay":         {"yellow": 12,   "red": 15},     # minutes
}

# Keywords que identifican sesiones en modo crisis
CRISIS_KEYWORDS = [
    "crisis", "modo crisis", "emergencia", "urgente",
    "examen mañana", "parcial mañana", "final mañana",
]

# ─── Carga de datos ─────────────────────────────────────────────────


def load_pomodoro_history() -> Dict:
    """Carga el historial de sesiones Pomodoro."""
    if not POMODORO_HISTORY.exists():
        return {"sessions": []}
    try:
        with open(POMODORO_HISTORY, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"sessions": []}


def load_semantic_memory() -> Dict:
    """Carga la memoria semántica (gists con scores)."""
    if not SEMANTIC_MEMORY.exists():
        return {"entries": []}
    try:
        with open(SEMANTIC_MEMORY, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"entries": []}


def filter_by_period(sessions: List[Dict], period: str) -> List[Dict]:
    """Filtra sesiones por período temporal."""
    today = datetime.now().date()

    if period == "today":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=today.weekday())  # Lunes
    elif period == "month":
        start_date = today - timedelta(days=30)
    else:
        start_date = today - timedelta(days=today.weekday())

    filtered = []
    for s in sessions:
        date_str = s.get("date", "")
        if date_str:
            try:
                session_date = datetime.fromisoformat(date_str).date()
                if session_date >= start_date:
                    filtered.append(s)
            except ValueError:
                pass
    return filtered


# ─── Cálculo de indicadores ─────────────────────────────────────────


def calc_abandonment_rate(sessions: List[Dict]) -> Tuple[Optional[float], str, str]:
    """
    Indicador 1: Tasa de abandono.
    Fórmula: Pomodoros abortados / Pomodoros iniciados.

    Actualmente history.json solo registra sesiones COMPLETADAS (cmd_stop no
    llama a record_session). Cuando el timer se mejore para registrar abortos
    con un campo "completed": false, este indicador se activará automáticamente.

    Por ahora: si existe el campo "completed" en alguna sesión, lo usa.
    Si no existe, reporta N/A con recomendación de upgrade.
    """
    if not sessions:
        return None, "⚪", "Sin datos"

    # Check if any session has the "completed" field (future enhancement)
    has_completion_data = any("completed" in s for s in sessions)

    if has_completion_data:
        total = len(sessions)
        aborted = sum(1 for s in sessions if s.get("completed") is False)
        rate = aborted / total if total > 0 else 0.0
        severity = classify_higher_is_worse(rate, THRESHOLDS["abandonment_rate"])
        detail = f"{aborted}/{total} abortados ({rate:.0%})"
        return rate, severity, detail
    else:
        # Todos los registros actuales son completados (el timer no registra abortos)
        completed = len(sessions)
        detail = f"{completed} completados (abortos no registrados aún — upgrade pomodoro_timer.py)"
        return None, "⚪", detail


def calc_consolidation_velocity(
    sessions: List[Dict], memory: Dict, period: str
) -> Tuple[Optional[float], str, str]:
    """
    Indicador 2: Velocidad de consolidación.
    Fórmula: Gists con score > 7 / Pomodoros completados.

    Lee gists de semantic_memory.json que tengan campo "score" (añadido en v2.2 Fase 1).
    Filtra por fecha si las entries tienen campo "date" o "created_at".
    """
    completed = len(sessions)
    if completed == 0:
        return None, "⚪", "Sin sesiones completadas"

    entries = memory.get("entries", [])
    # Count gists with score > 7 in the period
    today = datetime.now().date()
    if period == "today":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = today - timedelta(days=30)

    high_score_gists = 0
    total_gists_with_score = 0

    for entry in entries:
        score = entry.get("score")
        if score is None:
            continue

        # Try to filter by date if available
        entry_date_str = entry.get("date") or entry.get("created_at") or entry.get("timestamp")
        if entry_date_str:
            try:
                entry_date = datetime.fromisoformat(str(entry_date_str)).date()
                if entry_date < start_date:
                    continue
            except (ValueError, TypeError):
                pass  # No date filtering possible, include the entry

        total_gists_with_score += 1
        if score > 7:
            high_score_gists += 1

    if total_gists_with_score == 0:
        return None, "⚪", f"Sin gists con score en memoria semántica ({completed} pomodoros)"

    velocity = high_score_gists / completed
    severity = classify_lower_is_worse(velocity, THRESHOLDS["consolidation_velocity"])
    detail = f"{high_score_gists} gists score>7 / {completed} pomodoros = {velocity:.2f}"
    return velocity, severity, detail


def calc_crisis_ratio(sessions: List[Dict]) -> Tuple[Optional[float], str, str]:
    """
    Indicador 3: Ratio Modo Crisis.
    Fórmula: Pomodoros en crisis / total.

    Detecta sesiones de crisis por:
    1. Campo "crisis": true (si existe — future enhancement)
    2. Modo "exam_prep" o "ultradian" con keywords de crisis en el topic
    3. Topic contiene palabras clave de crisis
    """
    if not sessions:
        return None, "⚪", "Sin datos"

    crisis_count = 0
    for s in sessions:
        # Explicit crisis flag (future)
        if s.get("crisis") is True:
            crisis_count += 1
            continue

        topic_lower = (s.get("topic") or "").lower()
        mode = s.get("mode", "")

        # Check for crisis keywords in topic
        if any(kw in topic_lower for kw in CRISIS_KEYWORDS):
            crisis_count += 1
            continue

        # exam_prep mode often indicates pre-exam urgency
        if mode == "exam_prep":
            crisis_count += 1
            continue

    total = len(sessions)
    ratio = crisis_count / total if total > 0 else 0.0
    severity = classify_higher_is_worse(ratio, THRESHOLDS["crisis_ratio"])
    detail = f"{crisis_count}/{total} en crisis ({ratio:.0%})"
    return ratio, severity, detail


def calc_execution_gap(sessions: List[Dict]) -> Tuple[Optional[float], str, str]:
    """
    Indicador 4: Execution Gap.
    Fórmula: Planificados - Ejecutados.

    Requiere datos de planificación (campo "planned_pomodoros" en sesiones o
    un plan diario externo). Si no hay datos de planificación, infiere un
    baseline conservador basado en 5 días hábiles × 3 pomodoros/día = 15/semana.
    """
    executed = len(sessions)

    # Check if any session has planning data
    has_planning = any("planned_pomodoros" in s for s in sessions)

    if has_planning:
        planned = sum(s.get("planned_pomodoros", 0) for s in sessions)
        gap = max(0, planned - executed)
        severity = classify_higher_is_worse(gap, THRESHOLDS["execution_gap"])
        detail = f"Planificados: {planned}, Ejecutados: {executed}, Gap: {gap}"
        return float(gap), severity, detail
    else:
        # Baseline: 15 pomodoros/semana (5 días × 3 pomodoros)
        baseline = 15
        gap = max(0, baseline - executed)
        severity = classify_higher_is_worse(gap, THRESHOLDS["execution_gap"])
        detail = (
            f"Ejecutados: {executed}, Baseline: {baseline}/semana, "
            f"Gap: {gap} (baseline estimado — sin datos de planificación)"
        )
        return float(gap), severity, detail


def calc_recovery_decay(sessions: List[Dict]) -> Tuple[Optional[float], str, str]:
    """
    Indicador 5: Recovery Decay.
    Fórmula: Tiempo de descanso promedio.

    Requiere campo "break_duration_minutes" en las sesiones. Si no existe,
    estima basándose en el perfil del modo usado (short_break del config).

    > 15 min promedio indica descansos excesivos que fragmentan la concentración.
    """
    if not sessions:
        return None, "⚪", "Sin datos"

    has_break_data = any("break_duration_minutes" in s for s in sessions)

    if has_break_data:
        breaks = [
            s["break_duration_minutes"]
            for s in sessions
            if "break_duration_minutes" in s and s["break_duration_minutes"] is not None
        ]
        if not breaks:
            return None, "⚪", "Sin datos de descanso"
        avg = sum(breaks) / len(breaks)
        severity = classify_higher_is_worse(avg, THRESHOLDS["recovery_decay"])
        detail = f"Promedio: {avg:.1f} min ({len(breaks)} descansos registrados)"
        return avg, severity, detail
    else:
        # Estimate from mode profiles
        mode_breaks = {
            "default": 5, "intensive": 10, "light": 3,
            "exam_prep": 8, "ultradian": 20,
        }
        estimated_breaks = [
            mode_breaks.get(s.get("mode", "default"), 5) for s in sessions
        ]
        avg = sum(estimated_breaks) / len(estimated_breaks) if estimated_breaks else 5.0
        severity = classify_higher_is_worse(avg, THRESHOLDS["recovery_decay"])
        detail = f"Estimado: {avg:.1f} min (basado en perfiles de modo — sin registro real)"
        return avg, severity, detail


# ─── Clasificación de severidad ──────────────────────────────────────


def classify_higher_is_worse(value: float, thresholds: Dict) -> str:
    """Para métricas donde un valor ALTO es malo (abandono, crisis, gap, recovery)."""
    if value >= thresholds["red"]:
        return "🔴"
    elif value >= thresholds["yellow"]:
        return "🟡"
    else:
        return "🟢"


def classify_lower_is_worse(value: float, thresholds: Dict) -> str:
    """Para métricas donde un valor BAJO es malo (consolidación)."""
    if value <= thresholds["red"]:
        return "🔴"
    elif value <= thresholds["yellow"]:
        return "🟡"
    else:
        return "🟢"


# ─── Score compuesto ─────────────────────────────────────────────────


def compute_composite_score(indicators: List[Dict]) -> Tuple[int, str]:
    """
    Calcula un score compuesto de riesgo 0-100.

    Pesos:
      - Tasa de abandono:      25%
      - Consolidación:         20%
      - Ratio Crisis:          20%
      - Execution Gap:         20%
      - Recovery Decay:        15%

    Cada indicador se normaliza a 0-100 (100 = máximo riesgo).
    Los indicadores sin datos (None) se excluyen y se redistribuye el peso.
    """
    weights = {
        "abandonment_rate": 25,
        "consolidation_velocity": 20,
        "crisis_ratio": 20,
        "execution_gap": 20,
        "recovery_decay": 15,
    }

    active_weight = 0
    weighted_sum = 0

    for ind in indicators:
        key = ind["key"]
        value = ind["value"]
        if value is None:
            continue

        w = weights.get(key, 0)
        active_weight += w

        # Normalize each to 0-100 risk scale
        if key == "abandonment_rate":
            # 0% abandon = 0 risk, 50%+ = 100 risk
            risk = min(100, (value / 0.50) * 100)
        elif key == "consolidation_velocity":
            # 1.0+ velocity = 0 risk, 0.0 = 100 risk
            risk = max(0, min(100, (1.0 - value) * 100))
        elif key == "crisis_ratio":
            # 0% crisis = 0 risk, 100% = 100 risk
            risk = min(100, value * 100)
        elif key == "execution_gap":
            # 0 gap = 0 risk, 10+ gap = 100 risk
            risk = min(100, (value / 10.0) * 100)
        elif key == "recovery_decay":
            # 5 min avg = 0 risk, 25+ min = 100 risk
            risk = max(0, min(100, ((value - 5) / 20.0) * 100))
        else:
            risk = 50

        weighted_sum += risk * w

    if active_weight == 0:
        return 0, "⚪ Sin datos suficientes"

    composite = int(weighted_sum / active_weight)

    if composite >= 70:
        label = "🔴 RIESGO ALTO"
    elif composite >= 40:
        label = "🟡 RIESGO MEDIO"
    elif composite >= 10:
        label = "🟢 RIESGO BAJO"
    else:
        label = "🟢 EXCELENTE"

    return composite, label


# ─── Formateo de output ─────────────────────────────────────────────


def format_risk_report(indicators: List[Dict], composite: int, label: str, period: str) -> str:
    """Genera el bloque de texto para 'Resume semana'."""
    lines = []
    lines.append("")
    lines.append("┌" + "─" * 58 + "┐")
    lines.append(f"│  📊 SCORE DE RIESGO ACADÉMICO — Brain OS 2.2{' ' * 12}│")
    lines.append(f"│  Período: {period:<47}│")
    lines.append(f"│  Score: {composite}/100 — {label:<38}│")
    lines.append("├" + "─" * 58 + "┤")

    for ind in indicators:
        name = ind["name"]
        severity = ind["severity"]
        detail = ind["detail"]
        # Truncate detail to fit
        max_detail = 44
        if len(detail) > max_detail:
            detail = detail[:max_detail - 3] + "..."
        lines.append(f"│  {severity} {name:<24} {detail:<30}│")

    lines.append("├" + "─" * 58 + "┤")

    # Recommendations
    reds = [i for i in indicators if i["severity"] == "🔴"]
    yellows = [i for i in indicators if i["severity"] == "🟡"]
    grays = [i for i in indicators if i["severity"] == "⚪"]

    if reds:
        lines.append(f"│  ⚠️  ALERTAS ROJAS ({len(reds)}):{' ' * 38}│")
        for r in reds:
            rec = get_recommendation(r["key"])
            if len(rec) > 54:
                rec = rec[:51] + "..."
            lines.append(f"│    → {rec:<52}│")
    elif yellows:
        lines.append(f"│  📋 Atención en {len(yellows)} indicador(es) amarillo(s){' ' * 17}│")
    elif not grays:
        lines.append(f"│  ✅ Todos los indicadores en rango saludable{' ' * 12}│")

    if grays:
        lines.append(f"│  ℹ️  {len(grays)} indicador(es) sin datos suficientes{' ' * 17}│")

    lines.append("└" + "─" * 58 + "┘")

    return "\n".join(lines)


def get_recommendation(key: str) -> str:
    """Devuelve una recomendación breve para cada indicador en rojo."""
    recs = {
        "abandonment_rate": "Reducir interrupciones. Probar modo light si los bloques son largos.",
        "consolidation_velocity": "Más Active Recall post-sesión. Revisar calidad de gists.",
        "crisis_ratio": "Demasiado estudio reactivo. Planificar con study-router.",
        "execution_gap": "Planificar menos o ejecutar más. Ajustar baseline.",
        "recovery_decay": "Descansos excesivos. Usar timer estricto y evitar scroll.",
    }
    return recs.get(key, "Revisar indicador manualmente.")


def build_json_output(indicators: List[Dict], composite: int, label: str, period: str) -> Dict:
    """Genera output JSON para integración programática."""
    return {
        "risk_score": {
            "composite": composite,
            "label": label,
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "indicators": {
                ind["key"]: {
                    "value": ind["value"],
                    "severity": ind["severity"],
                    "detail": ind["detail"],
                }
                for ind in indicators
            },
        }
    }


# ─── Main ────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="📊 Risk Score — Indicadores de alerta temprana académica (Brain OS 2.2)"
    )
    parser.add_argument(
        "--period", "-p",
        choices=["today", "week", "month"],
        default="week",
        help="Período a analizar (default: week)",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output JSON en vez de texto formateado",
    )
    args = parser.parse_args()

    # Cargar datos
    history = load_pomodoro_history()
    memory = load_semantic_memory()

    # Filtrar sesiones por período
    sessions = filter_by_period(history.get("sessions", []), args.period)

    # Calcular los 5 indicadores
    ind1_val, ind1_sev, ind1_detail = calc_abandonment_rate(sessions)
    ind2_val, ind2_sev, ind2_detail = calc_consolidation_velocity(sessions, memory, args.period)
    ind3_val, ind3_sev, ind3_detail = calc_crisis_ratio(sessions)
    ind4_val, ind4_sev, ind4_detail = calc_execution_gap(sessions)
    ind5_val, ind5_sev, ind5_detail = calc_recovery_decay(sessions)

    indicators = [
        {"key": "abandonment_rate",       "name": "Tasa de abandono",      "value": ind1_val, "severity": ind1_sev, "detail": ind1_detail},
        {"key": "consolidation_velocity", "name": "Vel. consolidación",    "value": ind2_val, "severity": ind2_sev, "detail": ind2_detail},
        {"key": "crisis_ratio",           "name": "Ratio Modo Crisis",     "value": ind3_val, "severity": ind3_sev, "detail": ind3_detail},
        {"key": "execution_gap",          "name": "Execution Gap",         "value": ind4_val, "severity": ind4_sev, "detail": ind4_detail},
        {"key": "recovery_decay",         "name": "Recovery Decay",        "value": ind5_val, "severity": ind5_sev, "detail": ind5_detail},
    ]

    # Score compuesto
    composite, label = compute_composite_score(indicators)

    # Output
    if args.json:
        print(json.dumps(build_json_output(indicators, composite, label, args.period), indent=2, ensure_ascii=False))
    else:
        print(format_risk_report(indicators, composite, label, args.period))


if __name__ == "__main__":
    main()
