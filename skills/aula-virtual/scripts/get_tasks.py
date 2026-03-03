#!/usr/bin/env python3
"""
Script "Ojos de Águila" v2 - Buscador de Tareas UAndina
=======================================================
Este script hace cuatro cosas automáticamente:
1. Busca qué cursos estás llevando este semestre
2. Entra a cada uno para buscar tareas pendientes
3. Consulta el gradebook para calcular el peso de cada tarea
4. Asigna prioridad inteligente basada en urgencia + peso

Usage:
    python get_tasks.py
"""

import os
import requests
import json
from datetime import datetime
from pathlib import Path

# Cargar entorno
try:
    from dotenv import load_dotenv
    skill_dir = Path(__file__).parent.parent
    env_path = skill_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

TOKEN = os.getenv('MOODLE_TOKEN')
from course_map import MOODLE_URL
from moodle_api import MoodleAPI, MoodleAPIError
URL = os.getenv('MOODLE_URL', MOODLE_URL)
ENDPOINT = f"{URL}/webservice/rest/server.php"

# Cache de notas por curso para evitar llamadas duplicadas
_grades_cache: dict = {}


def call_moodle(function: str, params: dict = None) -> dict:
    """
    Llamada genérica a la API de Moodle.
    
    Args:
        function: Nombre de la función WS de Moodle
        params: Parámetros adicionales
        
    Returns:
        Respuesta JSON de Moodle
    """
    if params is None:
        params = {}
    
    params.update({
        'wstoken': TOKEN,
        'wsfunction': function,
        'moodlewsrestformat': 'json'
    })
    
    try:
        response = requests.post(ENDPOINT, data=params, timeout=30)
        return response.json()
    except Exception as e:
        return {'error': str(e)}


def get_assignment_weight(api: MoodleAPI, course_id: int, assignment_name: str) -> dict:
    """
    Obtiene el peso de una tarea en la nota final consultando el gradebook.
    
    Args:
        api: Instancia de MoodleAPI
        course_id: ID del curso en Moodle
        assignment_name: Nombre de la tarea para buscar en el gradebook
        
    Returns:
        Dict con 'weight' (float 0-100), 'grade' (nota actual), 'max_grade'
    """
    global _grades_cache
    
    # Usar cache si ya consultamos este curso
    if course_id not in _grades_cache:
        try:
            grades_data = api.get_grades(course_id)
            _grades_cache[course_id] = grades_data
        except MoodleAPIError:
            _grades_cache[course_id] = None
    
    grades_data = _grades_cache[course_id]
    if not grades_data:
        return {'weight': None, 'grade': None, 'max_grade': None}
    
    # Buscar el grade item que matchea la tarea por nombre
    for table in grades_data.get('usergrades', []):
        for item in table.get('gradeitems', []):
            item_name = item.get('itemname', '')
            if not item_name:
                continue
            
            # Match flexible: contiene el nombre o viceversa
            name_lower = assignment_name.lower()
            item_lower = item_name.lower()
            if name_lower in item_lower or item_lower in name_lower:
                weight_str = item.get('percentageformatted', '')
                weight = None
                if weight_str and weight_str != '-':
                    try:
                        weight = float(weight_str.replace('%', '').replace(',', '.').strip())
                    except ValueError:
                        pass
                
                return {
                    'weight': weight,
                    'grade': item.get('graderaw'),
                    'max_grade': item.get('grademax'),
                }
    
    return {'weight': None, 'grade': None, 'max_grade': None}


def calculate_urgency(days_remaining: int, weight: float = None) -> tuple:
    """
    Calcula score de urgencia y prioridad automática.
    
    Fórmula: urgencia = (peso_normalizado * 0.4) + (factor_tiempo * 0.6)
    
    Returns:
        Tuple (urgency_score: float, priority_label: str)
    """
    # Factor tiempo: inversamente proporcional a días restantes
    time_factor = 1.0 / max(days_remaining, 1)
    time_factor = min(time_factor, 1.0)  # Cap en 1.0
    
    # Factor peso: normalizado a 0-1 (si disponible)
    if weight is not None and weight > 0:
        weight_factor = weight / 100.0
    else:
        weight_factor = 0.3  # Default moderado si no hay data
    
    urgency = (weight_factor * 0.4) + (time_factor * 0.6)
    
    # Mapear a prioridad
    if urgency >= 0.5 or days_remaining <= 2:
        priority = "🔥 Alta"
    elif urgency >= 0.25 or days_remaining <= 7:
        priority = "⚡ Media"
    else:
        priority = "☁️ Baja"
    
    return urgency, priority


def get_pending_tasks(enrich_with_grades: bool = True) -> list:
    """
    Obtiene tareas pendientes con urgencia inteligente.
    
    Args:
        enrich_with_grades: Si True, consulta gradebook para peso de cada tarea
    
    Returns:
        Lista de tareas pendientes con peso, urgencia y prioridad auto-calculada
    """
    tasks = []
    current_time = datetime.now().timestamp()
    
    # Inicializar API para gradebook (si se pide enriquecimiento)
    api = None
    if enrich_with_grades:
        try:
            api = MoodleAPI()
        except (ValueError, MoodleAPIError):
            api = None
    
    # 1. Obtener mi ID de usuario
    site_info = call_moodle('core_webservice_get_site_info')
    if 'error' in site_info:
        return []
    
    user_id = site_info.get('userid')
    
    # 2. Obtener mis cursos
    courses = call_moodle('core_enrol_get_users_courses', {'userid': user_id})
    
    if not courses or 'error' in str(courses):
        return []
    
    # 3. Filtrar cursos recientes
    active_courses = courses[:15]
    course_ids = [c['id'] for c in active_courses]
    
    # 4. Obtener tareas
    params = {}
    for i, cid in enumerate(course_ids):
        params[f'courseids[{i}]'] = cid
    
    assignments_data = call_moodle('mod_assign_get_assignments', params)
    
    # 5. Procesar, enriquecer y filtrar
    for course in assignments_data.get('courses', []):
        course_name = course['fullname']
        course_id = course['id']
        
        for assign in course['assignments']:
            due_date = assign['duedate']
            if due_date > current_time:
                days_remaining = int((due_date - current_time) / (24 * 60 * 60))
                
                # Consultar peso en gradebook
                weight_info = {'weight': None, 'grade': None, 'max_grade': None}
                if api:
                    weight_info = get_assignment_weight(api, course_id, assign['name'])
                
                # Calcular urgencia
                urgency, auto_priority = calculate_urgency(days_remaining, weight_info['weight'])
                
                tasks.append({
                    'name': assign['name'],
                    'course': course_name,
                    'course_id': course_id,
                    'assignment_id': assign['id'],
                    'cmid': assign['cmid'],
                    'due_date': due_date,
                    'due_date_formatted': datetime.fromtimestamp(due_date).strftime('%d/%m/%Y %H:%M'),
                    'days_remaining': days_remaining,
                    'link': f"{URL}/mod/assign/view.php?id={assign['cmid']}",
                    'weight': weight_info['weight'],
                    'current_grade': weight_info['grade'],
                    'max_grade': weight_info['max_grade'],
                    'urgency_score': round(urgency, 3),
                    'auto_priority': auto_priority,
                })
    
    # Ordenar por urgencia (mayor primero)
    tasks.sort(key=lambda x: x['urgency_score'], reverse=True)
    
    return tasks


def main():
    """Función principal - Muestra tareas con prioridad inteligente."""
    
    if not TOKEN:
        print("❌ Error: No hay token configurado.")
        print("   Ejecuta primero: python get_uandina_token.py")
        return
    
    print("⏳ Conectando con UAndina para buscar tareas...")
    print("📊 Consultando gradebook para calcular prioridades...")
    
    tasks = get_pending_tasks(enrich_with_grades=True)
    
    print("\n" + "=" * 55)
    print("🚀 TAREAS PENDIENTES — Prioridad Inteligente")
    print("=" * 55)
    
    if not tasks:
        print("✅ ¡Eres libre! No hay tareas pendientes con fecha futura.")
        return
    
    for task in tasks:
        fecha = task['due_date_formatted']
        days = task['days_remaining']
        priority = task['auto_priority']
        weight = task['weight']
        urgency = task['urgency_score']
        
        # Emoji de prioridad
        if "Alta" in priority:
            emoji = "🔴"
        elif "Media" in priority:
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        # Formar línea de peso
        weight_str = f" | Peso: {weight:.0f}%" if weight else ""
        
        print(f"{emoji} {priority} [{fecha}] ({days}d){weight_str}")
        print(f"   📝 {task['name']}")
        print(f"   📖 {task['course']}")
        print(f"   🔗 {task['link']}")
        print("-" * 55)
    
    print(f"\n📊 Total pendientes: {len(tasks)}")
    print("💡 Prioridad: 🔴 Alta (peso alto / deadline cercano) | 🟡 Media | 🟢 Baja")
    print(f"📈 Urgencia calculada con fórmula: peso×0.4 + tiempo×0.6")


if __name__ == "__main__":
    main()
