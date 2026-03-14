#!/usr/bin/env python3
"""
Download Files — Moodle → Local
================================
Descarga archivos y URLs de todos los cursos mapeados en course_map.py.
Usa course_map.py como fuente de verdad para la cobertura de cursos.

Fixes aplicados:
  - FIX #4a: Reintentos automáticos (hasta 3 intentos, 2s entre cada uno)
  - FIX #4b: Detección de token expirado (Moodle devuelve HTML con status 200)
  - FIX #4c: Limpieza de archivos parciales/corruptos si la descarga falla

Usage:
    python download_files.py
"""

import re
import time
import requests
from pathlib import Path
from moodle_api import MoodleAPI
from course_map import COURSE_MAP, find_brain_os_course

# Número máximo de reintentos por archivo
MAX_RETRIES = 3
# Segundos de espera entre reintentos
RETRY_DELAY = 2

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

# =============================================================================
# FIX #4b: Detección de token expirado
# =============================================================================
def _is_token_expired_response(response: requests.Response) -> bool:
    """
    Detecta si Moodle devolvió un redirect de login en lugar del archivo.
    Ocurre cuando el token expiró — Moodle retorna HTML con status 200.
    """
    content_type = response.headers.get('Content-Type', '')
    if 'text/html' in content_type:
        return True  # Login redirect = token expirado
    if 'application/json' in content_type:
        try:
            data = response.json()
            if isinstance(data, dict) and ('error' in data or 'exception' in data):
                return True
        except Exception:
            pass
    return False

# =============================================================================
# FIX #4a + #4b + #4c: download_file con reintentos y limpieza
# =============================================================================
def download_file(url: str, token: str, dest_path: Path) -> bool:
    """
    Descarga un archivo desde Moodle con autenticación por token.

    Mejoras:
      - Hasta MAX_RETRIES intentos ante errores de red transitorios
      - Detecta token expirado (HTML con status 200) y aborta inmediatamente
      - Limpia el archivo parcial si la descarga no termina correctamente
    """
    params = {'token': token}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, params=params, stream=True, timeout=30)

            if response.status_code != 200:
                if attempt < MAX_RETRIES:
                    print(f"         ⚠️ HTTP {response.status_code}, reintento {attempt}/{MAX_RETRIES}...")
                    time.sleep(RETRY_DELAY)
                    continue
                return False

            # FIX #4b: Detectar token expirado ANTES de escribir el archivo
            if _is_token_expired_response(response):
                print("         ❌ Token expirado — Moodle respondió con página de login.")
                print("            Solución: python skills/aula-virtual/scripts/get_uandina_token.py")
                # No tiene sentido reintentar con token expirado
                return False

            # Escribir el archivo
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            return True

        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                print(f"         ⚠️ Timeout, reintento {attempt}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY)
            else:
                print("         ❌ Timeout tras todos los reintentos.")
                return False

        except requests.exceptions.ConnectionError:
            if attempt < MAX_RETRIES:
                print(f"         ⚠️ Error de conexión, reintento {attempt}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY)
            else:
                print("         ❌ Sin conexión tras todos los reintentos.")
                return False

        except requests.exceptions.RequestException as e:
            print(f"         ❌ Error inesperado: {e}")
            return False

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
    """Descarga un archivo si no existe localmente.
    FIX #4c: Si la descarga falla, limpia el archivo parcial para evitar corruptos.
    """
    clean_name = sanitize_filename(filename)
    full_path = dest_folder / clean_name

    if full_path.exists():
        return True

    full_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"      ⬇️ Descargando: {clean_name}...")

    success = download_file(file_url, token, full_path)

    if success:
        print(f"      ✅ Guardado.")
        return True
    else:
        # FIX #4c: Limpiar archivo parcial/corrupto
        if full_path.exists():
            full_path.unlink()
            print(f"      🗑️  Archivo parcial eliminado: {clean_name}")
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
