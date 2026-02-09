#!/usr/bin/env python3
"""
Script "Sabueso Digital" - Buscador de Recursos UAndina
=======================================================
Busca archivos y materiales en los cursos activos del aula virtual.
"""

import os
import requests
import json
from datetime import datetime
from pathlib import Path
from moodle_api import MoodleAPI

import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    output_file = Path("resources.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🦅 Recursos del Aula Virtual\n\n")
        
        try:
            api = MoodleAPI()
            
            # 1. Obtener cursos
            courses = api.get_courses()
            if not courses:
                f.write("❌ No se encontraron cursos.\n")
                return

            # Filtrar cursos recientes (top 10)
            active_courses = courses[:10]
            
            f.write(f"📚 Analizando {len(active_courses)} cursos recientes...\n\n")
            
            total_files = 0
            
            for course in active_courses:
                course_name = course['fullname']
                course_id = course['id']
                
                # Obtener contenidos
                contents = api.get_course_contents(course_id)
                
                found_in_course = False
                
                # Iterar secciones y moulos
                for section in contents:
                    section_name = section.get('name', 'General')
                    modules = section.get('modules', [])
                    
                    for module in modules:
                        mod_name = module.get('name')
                        mod_type = module.get('modname')
                        url = module.get('url', '')
                        
                        # Interesan: resource (archivos), folder, url
                        if mod_type in ['resource', 'folder', 'url']:
                            
                            # Si es recurso, intentar ver detalles del archivo
                            details = ""
                            if mod_type == 'resource':
                                files = module.get('contents', [])
                                if files:
                                    file_obj = files[0]
                                    f_size = file_obj.get('filesize', 0) / 1024 # KB
                                    f_ext = file_obj.get('filename', '').strip().split('.')[-1]
                                    details = f"({f_ext}, {f_size:.1f}KB)"
                            
                            if not found_in_course:
                                f.write(f"## 📘 {course_name}\n\n")
                                found_in_course = True
                                
                            icon = "📄" if mod_type == 'resource' else "📂" if mod_type == 'folder' else "🔗"
                            f.write(f"- {icon} **{mod_name}** {details}\n")
                            total_files += 1

            if total_files == 0:
                f.write("\n✅ No se encontraron archivos nuevos (o el sistema está vacío).\n")
            else:
                f.write(f"\n📦 **Total recursos encontrados:** {total_files}\n")
                
        except Exception as e:
            f.write(f"\n❌ Error: {e}\n")
            
    print(f"✅ Reporte generado: {output_file.absolute()}")

if __name__ == "__main__":
    main()
