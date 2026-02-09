#!/usr/bin/env python3
"""
Download Material Script
========================
Searches for a resource in Moodle courses and downloads it.
Usage:
    python download_material.py "search_term" [--course "course_name"] [--outdir "path/to/save"]
"""

import sys
import argparse
import requests
import re
from pathlib import Path
from moodle_api import MoodleAPI

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Download materials from Moodle.')
    parser.add_argument('query', help='Name of the file/resource to find')
    parser.add_argument('--course', help='Filter by course name (partial match)', default=None)
    parser.add_argument('--outdir', help='Output directory', default='.')
    
    args = parser.parse_args()
    
    print(f"🦅 Buscando recurso: '{args.query}'...")
    if args.course:
        print(f"   En curso: '{args.course}'")

    try:
        api = MoodleAPI()
        courses = api.get_courses()
        
        target_courses = []
        if args.course:
            for c in courses:
                if args.course.lower() in c['fullname'].lower():
                    target_courses.append(c)
        else:
            # Check recent/all courses if no filter
            target_courses = courses[:10] # Optimize by checking recent ones first

        found_resources = []

        for course in target_courses:
            # Skip if we already found exact matches, but might be good to find all
            contents = api.get_course_contents(course['id'])
            
            for section in contents:
                for module in section.get('modules', []):
                    # Check module name
                    mod_name = module.get('name', '')
                    
                    if args.query.lower() in mod_name.lower() and module.get('modname') == 'resource':
                        # Found a candidate
                        # Extract file details
                        contents_info = module.get('contents', [])
                        if contents_info:
                            file_data = contents_info[0]
                            file_url = file_data.get('fileurl')
                            original_filename = file_data.get('filename')
                            
                            found_resources.append({
                                'course': course['fullname'],
                                'name': mod_name,
                                'url': file_url,
                                'filename': original_filename,
                                'token': api.token
                            })

        if not found_resources:
            print("❌ No se encontraron recursos que coincidan.")
            return

        # If multiple found, ask or pick best (simple: duplicate check)
        print(f"✅ Se encontraron {len(found_resources)} coincidencias.")
        
        for res in found_resources:
            print(f"⬇️ Descargando: {res['name']} ({res['course']})")
            
            # Prepare download URL
            download_url = res['url']
            if "token=" not in download_url:
                download_url = f"{download_url}&token={res['token']}"
            
            # Prepare output path
            out_dir = Path(args.outdir)
            out_dir.mkdir(parents=True, exist_ok=True)
            
            clean_name = sanitize_filename(res['filename'])
            out_path = out_dir / clean_name
            
            # Download
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            with open(out_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"   💾 Guardado en: {out_path.absolute()}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
