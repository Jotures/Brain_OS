#!/usr/bin/env python3
"""
🍅 Pomodoro Timer - Brain OS Integration
Temporizador Pomodoro adaptativo controlado por el agente.

Uso:
    python pomodoro_timer.py start --topic "Tema" [--mode default|intensive|light|exam_prep]
    python pomodoro_timer.py pause
    python pomodoro_timer.py resume
    python pomodoro_timer.py stop
    python pomodoro_timer.py status
    python pomodoro_timer.py history [--period today|week|month]
    python pomodoro_timer.py suggest --topic "Tema"
"""

import argparse
import json
import os
import re
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# Directorio base del script
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
STATE_FILE = BASE_DIR / "state.json"
HISTORY_FILE = BASE_DIR / "history.json"
SOUNDS_DIR = BASE_DIR / "sounds"

# Intentar importar dependencias opcionales
try:
    from win10toast import ToastNotifier
    TOASTER = ToastNotifier()
    HAS_TOAST = True
except ImportError:
    HAS_TOAST = False
    TOASTER = None

try:
    from playsound import playsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False


def load_config() -> dict:
    """Carga la configuración desde config.json."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_state() -> dict:
    """Carga el estado actual desde state.json."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "status": "idle",
        "phase": "work",
        "cycle": 0,
        "topic": "",
        "mode": "default",
        "started_at": None,
        "ends_at": None,
        "paused_at": None,
        "remaining_seconds": None
    }


def save_state(state: dict) -> None:
    """Guarda el estado actual en state.json."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_history() -> dict:
    """Carga el historial desde history.json."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sessions": []}


def save_history(history: dict) -> None:
    """Guarda el historial en history.json."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def notify(title: str, message: str) -> None:
    """Envía una notificación de Windows."""
    config = load_config()
    if not config.get("notifications", {}).get("enabled", True):
        return
    
    if HAS_TOAST and TOASTER:
        try:
            TOASTER.show_toast(
                title,
                message,
                duration=5,
                threaded=True
            )
        except Exception as e:
            print(f"[WARN] No se pudo mostrar notificación: {e}")
    else:
        print(f"[NOTIFICATION] {title}: {message}")


def play_sound(sound_type: str) -> None:
    """Reproduce un sonido si está habilitado."""
    config = load_config()
    if not config.get("sounds", {}).get("enabled", True):
        return
    
    sound_file = config.get("sounds", {}).get(sound_type, "")
    sound_path = SOUNDS_DIR / sound_file
    
    if HAS_SOUND and sound_path.exists():
        try:
            playsound(str(sound_path))
        except Exception as e:
            print(f"[WARN] No se pudo reproducir sonido: {e}")
    else:
        # Usar beep del sistema como fallback
        print("\a")  # Bell character


def suggest_mode(topic: str) -> str:
    """Sugiere un modo basado en el tema usando reglas de config."""
    config = load_config()
    rules = config.get("adaptive_suggestions", {}).get("rules", {})
    
    topic_lower = topic.lower()
    for pattern, mode in rules.items():
        if re.search(pattern, topic_lower):
            return mode
    
    return "default"


def format_time(seconds: int) -> str:
    """Formatea segundos como MM:SS."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def get_duration(mode: str, phase: str) -> int:
    """Obtiene la duración en segundos para un modo y fase."""
    config = load_config()
    profile = config.get("profiles", {}).get(mode, config.get("profiles", {}).get("default", {}))
    
    if phase == "work":
        return profile.get("work_duration", 25) * 60
    elif phase == "short_break":
        return profile.get("short_break", 5) * 60
    elif phase == "long_break":
        return profile.get("long_break", 15) * 60
    
    return 25 * 60  # Fallback


def run_timer(duration_seconds: int, phase: str, topic: str) -> bool:
    """
    Ejecuta el temporizador en background.
    Retorna True si completó, False si fue interrumpido.
    """
    state = load_state()
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=duration_seconds)
    
    state["started_at"] = start_time.isoformat()
    state["ends_at"] = end_time.isoformat()
    state["status"] = "running"
    save_state(state)
    
    phase_emoji = "🍅" if phase == "work" else "☕"
    phase_name = "Trabajo" if phase == "work" else "Descanso"
    notify(f"{phase_emoji} Pomodoro - {phase_name}", f"Tema: {topic}\nDuración: {format_time(duration_seconds)}")
    
    remaining = duration_seconds
    while remaining > 0:
        state = load_state()
        
        # Verificar si fue pausado o detenido
        if state["status"] == "paused":
            state["remaining_seconds"] = remaining
            save_state(state)
            return False
        
        if state["status"] == "stopped" or state["status"] == "idle":
            return False
        
        time.sleep(1)
        remaining -= 1
        
        # Actualizar estado cada 10 segundos
        if remaining % 10 == 0:
            state["remaining_seconds"] = remaining
            save_state(state)
    
    # Timer completado
    sound_type = "work_end" if phase == "work" else "break_end"
    play_sound(sound_type)
    
    completion_emoji = "✅" if phase == "work" else "🔔"
    completion_msg = "¡Tiempo de descanso!" if phase == "work" else "¡Vuelve al trabajo!"
    notify(f"{completion_emoji} Pomodoro completado", completion_msg)
    
    return True


def cmd_start(args) -> None:
    """Inicia una nueva sesión de Pomodoro."""
    state = load_state()
    
    if state["status"] == "running":
        print(json.dumps({"error": "Ya hay un Pomodoro en ejecución", "current_topic": state["topic"]}))
        return
    
    topic = args.topic or "Sin tema"
    mode = args.mode
    
    # Si no se especifica modo, sugerir uno
    if not mode or mode == "auto":
        mode = suggest_mode(topic)
        print(json.dumps({"info": f"Modo sugerido: {mode}"}))
    
    config = load_config()
    cycles_for_long = config.get("cycles_before_long_break", 4)
    
    state = {
        "status": "running",
        "phase": "work",
        "cycle": 1,
        "topic": topic,
        "mode": mode,
        "started_at": datetime.now().isoformat(),
        "ends_at": None,
        "paused_at": None,
        "remaining_seconds": None,
        "session_start": datetime.now().isoformat()
    }
    save_state(state)
    
    duration = get_duration(mode, "work")
    if args.debug_duration:
        duration = args.debug_duration  # Para testing
    
    print(json.dumps({
        "status": "started",
        "topic": topic,
        "mode": mode,
        "duration_minutes": duration // 60,
        "cycle": 1
    }))
    
    # Ejecutar el timer (esto bloquea hasta completar o interrumpir)
    completed = run_timer(duration, "work", topic)
    
    if completed:
        state = load_state()
        state["phase"] = "short_break" if state["cycle"] < cycles_for_long else "long_break"
        state["status"] = "break_pending"
        save_state(state)
        
        # Registrar pomodoro completado
        record_session(topic, mode, "work", duration // 60)
        
        print(json.dumps({
            "status": "work_complete",
            "next_phase": state["phase"],
            "cycle": state["cycle"]
        }))


def cmd_pause(args) -> None:
    """Pausa el Pomodoro actual."""
    state = load_state()
    
    if state["status"] != "running":
        print(json.dumps({"error": "No hay Pomodoro en ejecución"}))
        return
    
    state["status"] = "paused"
    state["paused_at"] = datetime.now().isoformat()
    save_state(state)
    
    notify("⏸️ Pomodoro pausado", f"Tema: {state['topic']}")
    print(json.dumps({"status": "paused", "topic": state["topic"]}))


def cmd_resume(args) -> None:
    """Reanuda un Pomodoro pausado."""
    state = load_state()
    
    if state["status"] != "paused":
        print(json.dumps({"error": "No hay Pomodoro pausado"}))
        return
    
    remaining = state.get("remaining_seconds", 0)
    if remaining <= 0:
        print(json.dumps({"error": "No hay tiempo restante"}))
        return
    
    state["status"] = "running"
    state["paused_at"] = None
    save_state(state)
    
    notify("▶️ Pomodoro reanudado", f"Tiempo restante: {format_time(remaining)}")
    print(json.dumps({"status": "resumed", "remaining_seconds": remaining}))
    
    # Continuar el timer
    run_timer(remaining, state["phase"], state["topic"])


def cmd_stop(args) -> None:
    """Detiene el Pomodoro actual."""
    state = load_state()
    
    if state["status"] == "idle":
        print(json.dumps({"error": "No hay Pomodoro activo"}))
        return
    
    # Calcular tiempo trabajado
    if state.get("session_start"):
        start = datetime.fromisoformat(state["session_start"])
        worked_minutes = (datetime.now() - start).seconds // 60
    else:
        worked_minutes = 0
    
    old_topic = state["topic"]
    old_cycle = state["cycle"]
    
    # Reset state
    state = {
        "status": "idle",
        "phase": "work",
        "cycle": 0,
        "topic": "",
        "mode": "default",
        "started_at": None,
        "ends_at": None,
        "paused_at": None,
        "remaining_seconds": None
    }
    save_state(state)
    
    notify("🛑 Pomodoro detenido", f"Trabajaste {worked_minutes} minutos")
    print(json.dumps({
        "status": "stopped",
        "topic": old_topic,
        "cycles_completed": old_cycle - 1,
        "worked_minutes": worked_minutes
    }))


def cmd_status(args) -> None:
    """Muestra el estado actual del Pomodoro."""
    state = load_state()
    config = load_config()
    
    output = {
        "status": state["status"],
        "phase": state["phase"],
        "cycle": state["cycle"],
        "topic": state["topic"],
        "mode": state["mode"]
    }
    
    if state["status"] == "running" and state.get("ends_at"):
        end_time = datetime.fromisoformat(state["ends_at"])
        remaining = max(0, (end_time - datetime.now()).seconds)
        output["remaining"] = format_time(remaining)
        output["remaining_seconds"] = remaining
    
    if state["status"] == "paused" and state.get("remaining_seconds"):
        output["remaining"] = format_time(state["remaining_seconds"])
        output["remaining_seconds"] = state["remaining_seconds"]
    
    print(json.dumps(output))


def cmd_history(args) -> None:
    """Muestra el historial de sesiones."""
    history = load_history()
    period = args.period or "today"
    
    today = datetime.now().date()
    
    if period == "today":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=7)
    elif period == "month":
        start_date = today - timedelta(days=30)
    else:
        start_date = today
    
    filtered = [
        s for s in history.get("sessions", [])
        if datetime.fromisoformat(s["date"]).date() >= start_date
    ]
    
    total_pomodoros = sum(s.get("cycles_completed", 1) for s in filtered)
    total_minutes = sum(s.get("duration_minutes", 25) for s in filtered)
    
    print(json.dumps({
        "period": period,
        "total_sessions": len(filtered),
        "total_pomodoros": total_pomodoros,
        "total_focus_minutes": total_minutes,
        "sessions": filtered[-10:]  # Últimas 10
    }))


def cmd_suggest(args) -> None:
    """Sugiere un modo basado en el tema."""
    topic = args.topic or ""
    mode = suggest_mode(topic)
    config = load_config()
    profile = config.get("profiles", {}).get(mode, {})
    
    print(json.dumps({
        "topic": topic,
        "suggested_mode": mode,
        "description": profile.get("description", ""),
        "work_duration": profile.get("work_duration", 25),
        "short_break": profile.get("short_break", 5)
    }))


def record_session(topic: str, mode: str, phase: str, duration_minutes: int) -> None:
    """Registra una sesión completada en el historial."""
    history = load_history()
    
    session = {
        "date": datetime.now().isoformat(),
        "topic": topic,
        "mode": mode,
        "phase": phase,
        "duration_minutes": duration_minutes,
        "synced_to_notion": False
    }
    
    history["sessions"].append(session)
    save_history(history)


def main():
    parser = argparse.ArgumentParser(
        description="🍅 Pomodoro Timer - Brain OS",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # start
    start_parser = subparsers.add_parser("start", help="Iniciar Pomodoro")
    start_parser.add_argument("--topic", "-t", type=str, help="Tema de estudio")
    start_parser.add_argument("--mode", "-m", type=str, 
                              choices=["default", "intensive", "light", "exam_prep", "auto"],
                              default="auto", help="Modo de duración")
    start_parser.add_argument("--debug-duration", type=int, help="Duración en segundos (debug)")
    
    # pause
    subparsers.add_parser("pause", help="Pausar Pomodoro")
    
    # resume
    subparsers.add_parser("resume", help="Reanudar Pomodoro")
    
    # stop
    subparsers.add_parser("stop", help="Detener Pomodoro")
    
    # status
    subparsers.add_parser("status", help="Ver estado actual")
    
    # history
    history_parser = subparsers.add_parser("history", help="Ver historial")
    history_parser.add_argument("--period", "-p", type=str,
                                choices=["today", "week", "month"],
                                default="today", help="Período a mostrar")
    
    # suggest
    suggest_parser = subparsers.add_parser("suggest", help="Sugerir modo para tema")
    suggest_parser.add_argument("--topic", "-t", type=str, required=True, help="Tema")
    
    args = parser.parse_args()
    
    if args.command == "start":
        cmd_start(args)
    elif args.command == "pause":
        cmd_pause(args)
    elif args.command == "resume":
        cmd_resume(args)
    elif args.command == "stop":
        cmd_stop(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "history":
        cmd_history(args)
    elif args.command == "suggest":
        cmd_suggest(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
