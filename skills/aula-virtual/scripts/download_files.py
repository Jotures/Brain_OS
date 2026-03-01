#!/usr/bin/env python3
"""
Download Files — Moodle → Local
================================
Descarga archivos y URLs de todos los cursos mapeados en course_map.py.
Usa course_map.py como fuente de verdad para la cobertura de cursos.

Usage:
    python download_files.py
"""

import re
import requests
from pathlib import Path
from moodle_api import MoodleAPI
from course_map import COURSE_MAP, find_brain_os_course

BASE_PATH = Path("c:/Users/Ruben J/Documents/Antigravito Proyects/Brain_OS/carrera/semestres/2026-1/cursos")
PERSONAL_PATH = Path("c:/Users/Ruben J/Documents/Antigravito Proyects/Brain_OS/cursos_personales")


def sanitize_filename(filename: str) -> str:
    """Limpia caracteres no válidos del nombre de archivo."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def get_base_path(course_info: dict) -> Path:
    """Retorna la ruta base según si es curso universitario o personal."""
    if course_info.get('is_personal'):
        return PERSONAL_PATH
    return BASE_PATH


def download_file(url: str, token: str, dest_path: Path) -> bool:
    """Descarga un archivo desde Moodle con autenticación por token."""
    try:
        params = {'token': token}
        response = requests.get(url, params=params, stream=True)
        if response.status_code == 200:
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            return True
    except requests.exceptions.RequestException:
        pass
    return False


def create_url_shortcut(filename: str, target_url: str, dest_folder: Path) -> None:
    """Crea un acceso directo .url para enlaces externos de Moodle."""
    full_path = dest_folder / filename
    if full_path.exists():
        return

    full_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(full_path, "w") as f:
            f.write("[InternetShortcut]\n")
            f.write(f"URL={target_url}\n")
        print(f"      🔗 Link creado: {filename}")
    except Exception as e:
        print(f"      ❌ Error creando link: {e}")


def process_file_download(filename: str, file_url: str, dest_folder: Path, token: str) -> bool:
    """Descarga un archivo si no existe localmente."""
    clean_name = sanitize_filename(filename)
    full_path = dest_folder / clean_name

    if full_path.exists():
        return True

    full_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"      ⬇️ Descargando: {clean_name}...")
    if download_file(file_url, token, full_path):
        print(f"      ✅ Guardado.")
        return True
    else:
        print(f"      ❌ Error en descarga.")
        return False


def main():
    api = MoodleAPI()
    print("🚀 Iniciando Sincronización Moodle → Local (Automática)...")

    stats = {'found': 0, 'downloaded': 0, 'skipped': 0, 'errors': 0}

    try:
        courses = api.get_courses()

        for course in courses:
            moodle_name = course['fullname']
            course_info = find_brain_os_course(moodle_name)

            if not course_info:
                continue

            local_folder = course_info.get('local_folder')
            if not local_folder:
                print(f"   ⚠️ Sin carpeta local para: {course_info['name']}")
                continue

            base = get_base_path(course_info)
            dest_folder = base / local_folder

            print(f"\n{course_info['emoji']} Procesando: {course_info['name']}")

            contents = api.get_course_contents(course['id'])

            for section in contents:
                for module in section.get('modules', []):
                    mod_name = module.get('modname')

                    if mod_name == 'resource':
                        for content in module.get('contents', []):
                            if content.get('type') == 'file':
                                stats['found'] += 1
                                filename = content.get('filename')
                                file_url = content.get('fileurl')
                                if process_file_download(filename, file_url, dest_folder, api.token):
                                    stats['downloaded'] += 1
                                else:
                                    stats['errors'] += 1

                    elif mod_name == 'url':
                        url_contents = module.get('contents', [])
                        if url_contents:
                            target_url = url_contents[0].get('fileurl')
                            safe_name = re.sub(r'[<>:"/\\|?*]', '', module.get('name', 'link'))
                            filename = f"{safe_name.strip()}.url"
                            create_url_shortcut(filename, target_url, dest_folder)

        print("\n" + "=" * 50)
        print(f"🏁 Sincronización finalizada.")
        print(f"   Encontrados: {stats['found']}")
        print(f"   Descargados: {stats['downloaded']}")
        print(f"   Errores:     {stats['errors']}")

    except Exception as e:
        print(f"❌ Error General: {e}")


if __name__ == "__main__":
    main()
