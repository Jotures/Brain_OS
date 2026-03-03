#!/usr/bin/env python3
"""
Watcher de Materiales — Brain OS
=================================
Detecta materiales nuevos subidos a Moodle desde la última sincronización.
Mantiene un estado persistente en data/materials_state.json para
identificar qué archivos son nuevos.

Usage:
    python watch_materials.py                # Detectar y descargar nuevos
    python watch_materials.py --detect-only  # Solo reportar, no descargar
    python watch_materials.py --reset        # Resetear estado (re-escanear todo)
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List

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
from download_files import process_file_download, create_url_shortcut, get_base_path, sanitize_filename

# Estado persistente
STATE_FILE = Path(__file__).parent / "data" / "materials_state.json"

BASE_PATH = Path("c:/Users/Ruben J/Documents/Antigravito Proyects/Brain_OS/carrera/semestres/2026-1/cursos")
PERSONAL_PATH = Path("c:/Users/Ruben J/Documents/Antigravito Proyects/Brain_OS/cursos_personales")


def load_state() -> Dict:
    """Carga el estado persistente de materiales conocidos."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    return {
        "last_run": None,
        "known_files": {}
    }


def save_state(state: Dict) -> None:
    """Guarda el estado persistente."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_run"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def generate_file_key(course_id: int, filename: str, fileurl: str) -> str:
    """Genera una clave única para identificar un archivo."""
    return f"{course_id}:{filename}:{fileurl}"


def detect_new_materials(api: MoodleAPI, state: Dict) -> List[Dict]:
    """
    Compara archivos actuales en Moodle contra el estado guardado.
    
    Returns:
        Lista de archivos nuevos con metadata para descarga
    """
    new_files = []
    known = state.get("known_files", {})
    courses = api.get_courses()
    
    for course in courses:
        moodle_name = course['fullname']
        course_info = find_brain_os_course(moodle_name)
        
        if not course_info:
            continue
        
        course_id = course['id']
        
        try:
            contents = api.get_course_contents(course_id)
        except MoodleAPIError:
            continue
        
        for section in contents:
            for module in section.get('modules', []):
                mod_name = module.get('modname', '')
                
                if mod_name == 'resource':
                    for content in module.get('contents', []):
                        if content.get('type') != 'file':
                            continue
                        
                        filename = content.get('filename', '')
                        fileurl = content.get('fileurl', '')
                        timemodified = content.get('timemodified', 0)
                        
                        key = generate_file_key(course_id, filename, fileurl)
                        
                        # Verificar si es nuevo o fue modificado
                        if key not in known:
                            new_files.append({
                                'filename': filename,
                                'fileurl': fileurl,
                                'timemodified': timemodified,
                                'course_id': course_id,
                                'course_info': course_info,
                                'key': key,
                                'type': 'file',
                            })
                        elif known[key].get('timemodified', 0) < timemodified:
                            new_files.append({
                                'filename': filename,
                                'fileurl': fileurl,
                                'timemodified': timemodified,
                                'course_id': course_id,
                                'course_info': course_info,
                                'key': key,
                                'type': 'file_updated',
                            })
                
                elif mod_name == 'url':
                    url_contents = module.get('contents', [])
                    if url_contents:
                        target_url = url_contents[0].get('fileurl', '')
                        link_name = module.get('name', 'link')
                        safe_name = re.sub(r'[<>:"/\\|?*]', '', link_name)
                        filename = f"{safe_name.strip()}.url"
                        
                        key = generate_file_key(course_id, filename, target_url)
                        
                        if key not in known:
                            new_files.append({
                                'filename': filename,
                                'fileurl': target_url,
                                'timemodified': 0,
                                'course_id': course_id,
                                'course_info': course_info,
                                'key': key,
                                'type': 'url',
                            })
    
    return new_files


def download_new_materials(new_files: List[Dict], api: MoodleAPI, state: Dict) -> Dict:
    """
    Descarga los archivos nuevos y actualiza el estado.
    
    Returns:
        Estadísticas de descarga
    """
    stats = {'downloaded': 0, 'urls_created': 0, 'errors': 0}
    
    for file_info in new_files:
        course_info = file_info['course_info']
        local_folder = course_info.get('local_folder')
        
        if not local_folder:
            continue
        
        # Determinar ruta base
        if course_info.get('is_personal'):
            base = PERSONAL_PATH
        else:
            base = BASE_PATH
        
        dest_folder = base / local_folder
        
        if file_info['type'] == 'url':
            create_url_shortcut(file_info['filename'], file_info['fileurl'], dest_folder)
            stats['urls_created'] += 1
        else:
            success = process_file_download(
                file_info['filename'],
                file_info['fileurl'],
                dest_folder,
                api.token
            )
            if success:
                stats['downloaded'] += 1
            else:
                stats['errors'] += 1
        
        # Registrar en el estado
        state["known_files"][file_info['key']] = {
            'filename': file_info['filename'],
            'timemodified': file_info['timemodified'],
            'course': course_info['name'],
            'first_seen': datetime.now().isoformat(),
        }
    
    return stats


def register_all_current(api: MoodleAPI, state: Dict) -> int:
    """Registra todos los archivos actuales como conocidos sin descargar."""
    count = 0
    courses = api.get_courses()
    
    for course in courses:
        course_info = find_brain_os_course(course['fullname'])
        if not course_info:
            continue
        
        try:
            contents = api.get_course_contents(course['id'])
        except MoodleAPIError:
            continue
        
        for section in contents:
            for module in section.get('modules', []):
                mod_name = module.get('modname', '')
                
                if mod_name == 'resource':
                    for content in module.get('contents', []):
                        if content.get('type') != 'file':
                            continue
                        key = generate_file_key(course['id'], content.get('filename', ''), content.get('fileurl', ''))
                        if key not in state["known_files"]:
                            state["known_files"][key] = {
                                'filename': content.get('filename'),
                                'timemodified': content.get('timemodified', 0),
                                'course': course_info['name'],
                                'first_seen': datetime.now().isoformat(),
                            }
                            count += 1
                
                elif mod_name == 'url':
                    url_contents = module.get('contents', [])
                    if url_contents:
                        target_url = url_contents[0].get('fileurl', '')
                        link_name = module.get('name', 'link')
                        safe_name = re.sub(r'[<>:"/\\|?*]', '', link_name)
                        filename = f"{safe_name.strip()}.url"
                        key = generate_file_key(course['id'], filename, target_url)
                        if key not in state["known_files"]:
                            state["known_files"][key] = {
                                'filename': filename,
                                'timemodified': 0,
                                'course': course_info['name'],
                                'first_seen': datetime.now().isoformat(),
                            }
                            count += 1
    
    return count


def main():
    parser = argparse.ArgumentParser(description='Watcher de materiales nuevos en Moodle')
    parser.add_argument('--detect-only', action='store_true', help='Solo reportar, no descargar')
    parser.add_argument('--reset', action='store_true', help='Resetear estado')
    args = parser.parse_args()
    
    try:
        api = MoodleAPI()
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    state = load_state()
    is_first_run = state["last_run"] is None
    
    # Reset si se pide
    if args.reset:
        state = {"last_run": None, "known_files": {}}
        is_first_run = True
        print("🔄 Estado reseteado.")
    
    print("👁️ Watcher de Materiales — Brain OS")
    print("=" * 50)
    
    if is_first_run:
        print("📋 Primera ejecución: registrando archivos existentes...")
        count = register_all_current(api, state)
        save_state(state)
        print(f"✅ Registrados {count} archivos como conocidos.")
        print("💡 En la próxima ejecución se detectarán archivos nuevos.")
        return
    
    print(f"📅 Última verificación: {state['last_run']}")
    print(f"📂 Archivos conocidos: {len(state['known_files'])}")
    print("\n🔍 Buscando materiales nuevos...")
    
    new_files = detect_new_materials(api, state)
    
    if not new_files:
        print("\n✅ No se encontraron materiales nuevos.")
        save_state(state)
        return
    
    # Agrupar nuevos por curso
    by_course = {}
    for f in new_files:
        cname = f['course_info']['name']
        by_course.setdefault(cname, []).append(f)
    
    print(f"\n🆕 Se encontraron {len(new_files)} materiales nuevos en {len(by_course)} cursos:\n")
    
    for course_name, files in by_course.items():
        emoji = files[0]['course_info']['emoji']
        print(f"{emoji} {course_name}:")
        for f in files:
            tag = "🔄 Actualizado" if f['type'] == 'file_updated' else "🆕 Nuevo"
            print(f"   {tag}: {f['filename']}")
    
    if args.detect_only:
        print(f"\n📋 Modo detect-only: no se descargó nada.")
        # Aún así guardar estado
        save_state(state)
        return
    
    # Descargar
    print(f"\n⬇️ Descargando {len(new_files)} archivos nuevos...")
    stats = download_new_materials(new_files, api, state)
    save_state(state)
    
    print(f"\n🏁 Descarga completada:")
    print(f"   📥 Archivos descargados: {stats['downloaded']}")
    print(f"   🔗 URLs creados: {stats['urls_created']}")
    if stats['errors']:
        print(f"   ❌ Errores: {stats['errors']}")


if __name__ == "__main__":
    main()
