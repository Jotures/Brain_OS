#!/usr/bin/env python3
"""
Script "Ojos de Águila" - Buscador de Tareas UAndina
====================================================
Este script hace tres cosas automáticamente:
1. Busca qué cursos estás llevando este semestre
2. Entra a cada uno para buscar tareas pendientes
3. Da un resumen limpio (filtra tareas antiguas)

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
URL = os.getenv('MOODLE_URL', 'https://campus.uandina.edu.pe')
ENDPOINT = f"{URL}/webservice/rest/server.php"


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


def get_pending_tasks() -> list:
    """
    Obtiene todas las tareas pendientes de los cursos activos.
    
    Returns:
        Lista de tareas pendientes con fecha futura
    """
    tasks = []
    current_time = datetime.now().timestamp()
    
    # 1. Obtener mi ID de usuario
    site_info = call_moodle('core_webservice_get_site_info')
    if 'error' in site_info:
        return []
    
    user_id = site_info.get('userid')
    
    # 2. Obtener mis cursos
    courses = call_moodle('core_enrol_get_users_courses', {'userid': user_id})
    
    if not courses or 'error' in str(courses):
        return []
    
    # 3. Filtrar cursos recientes (últimos 15 para evitar años pasados)
    active_courses = courses[:15]
    course_ids = [c['id'] for c in active_courses]
    
    # 4. Obtener tareas de esos cursos
    # Moodle pide los IDs en formato array: courseids[0]=X, courseids[1]=Y...
    params = {}
    for i, cid in enumerate(course_ids):
        params[f'courseids[{i}]'] = cid
    
    assignments_data = call_moodle('mod_assign_get_assignments', params)
    
    # 5. Procesar y filtrar tareas futuras
    for course in assignments_data.get('courses', []):
        course_name = course['fullname']
        for assign in course['assignments']:
            due_date = assign['duedate']
            # Solo tareas que vencen en el futuro
            if due_date > current_time:
                tasks.append({
                    'name': assign['name'],
                    'course': course_name,
                    'course_id': course['id'],
                    'assignment_id': assign['id'],
                    'cmid': assign['cmid'],
                    'due_date': due_date,
                    'due_date_formatted': datetime.fromtimestamp(due_date).strftime('%d/%m/%Y %H:%M'),
                    'days_remaining': int((due_date - current_time) / (24 * 60 * 60)),
                    'link': f"{URL}/mod/assign/view.php?id={assign['cmid']}"
                })
    
    # Ordenar por fecha de vencimiento
    tasks.sort(key=lambda x: x['due_date'])
    
    return tasks


def main():
    """Función principal - Muestra tareas pendientes."""
    
    if not TOKEN:
        print("❌ Error: No hay token configurado.")
        print("   Ejecuta primero: python get_uandina_token.py")
        return
    
    print("⏳ Conectando con UAndina para buscar tareas...")
    
    # 1. Obtener mi ID de usuario
    site_info = call_moodle('core_webservice_get_site_info')
    
    if 'error' in site_info:
        print(f"❌ Error de conexión: {site_info.get('error')}")
        return
    
    user_id = site_info['userid']
    print(f"👤 Usuario: {site_info.get('fullname', 'N/A')}")
    
    # 2. Obtener mis cursos
    print("📚 Buscando cursos...")
    courses = call_moodle('core_enrol_get_users_courses', {'userid': user_id})
    
    if not courses:
        print("❌ No se encontraron cursos.")
        return
    
    # 3. Filtrar cursos recientes (para evitar cursos de años pasados)
    active_courses = courses[:15]
    course_ids = [c['id'] for c in active_courses]
    
    # 4. Obtener tareas de esos cursos
    print(f"🔍 Escaneando {len(course_ids)} cursos en busca de tareas...")
    
    # Moodle pide los IDs en formato array: courseids[0]=X, courseids[1]=Y...
    params = {}
    for i, cid in enumerate(course_ids):
        params[f'courseids[{i}]'] = cid
    
    assignments_data = call_moodle('mod_assign_get_assignments', params)
    
    # 5. Procesar y mostrar
    found_tasks = 0
    current_time = datetime.now().timestamp()
    
    print("\n" + "=" * 50)
    print("🚀 TAREAS PENDIENTES (U ANDINA)")
    print("=" * 50)
    
    for course in assignments_data.get('courses', []):
        course_name = course['fullname']
        for assign in course['assignments']:
            # Solo mostrar tareas que vencen en el futuro
            due_date = assign['duedate']
            if due_date > current_time:
                found_tasks += 1
                fecha = datetime.fromtimestamp(due_date).strftime('%d/%m/%Y %H:%M')
                days_left = int((due_date - current_time) / (24 * 60 * 60))
                
                # Emoji según urgencia
                if days_left <= 2:
                    emoji = "🔴"
                elif days_left <= 7:
                    emoji = "🟡"
                else:
                    emoji = "🟢"
                
                print(f"{emoji} [{fecha}] ({days_left}d) {assign['name']}")
                print(f"   📖 {course_name}")
                print(f"   🔗 {URL}/mod/assign/view.php?id={assign['cmid']}")
                print("-" * 50)
    
    if found_tasks == 0:
        print("✅ ¡Eres libre! No hay tareas pendientes con fecha futura.")
    else:
        print(f"\n📊 Total pendientes: {found_tasks}")
        print("\n💡 Colores: 🔴 Urgente (≤2d) | 🟡 Pronto (≤7d) | 🟢 Normal")


if __name__ == "__main__":
    main()
