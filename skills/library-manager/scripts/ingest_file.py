#!/usr/bin/env python3
"""
Ingest File Script for Brain OS
===============================
Moves a file to the appropriate course folder and registers it in Notion.

Usage:
    python ingest_file.py --file "path/to/file.pdf" --course "Economia Ambiental"
"""

import os
import sys
import shutil
import argparse
import json
import subprocess
from datetime import datetime

# =============================================================================
# CONFIGUTATION & CONSTANTS
# =============================================================================

# Importar IDs centralizados desde course_map.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "aula-virtual", "scripts"))
from course_map import NOTION_DB_RECURSOS, COURSE_MAP as _COURSE_MAP, find_brain_os_course

# Base Paths (Adjust as needed)
BASE_DIR = r"C:\Users\Ruben J\Documents\Antigravito Proyects\Brain_OS"
UNI_DIR = os.path.join(BASE_DIR, "carrera", "semestres", "2026-1", "cursos")
PERSONAL_DIR = os.path.join(BASE_DIR, "cursos_personales")

# =============================================================================
# HELPERS
# =============================================================================

def find_course(query: str) -> dict | None:
    """Busca un curso usando course_map.py centralizado. Retorna dict compatible."""
    # Intentar match directo por key
    query_upper = query.upper()
    for key, info in _COURSE_MAP.items():
        if key.upper() == query_upper:
            return {
                'folder': info['local_folder'].split('/')[0],
                'notion_id': info['notion_id'],
                'type': 'personal' if info.get('is_personal') else 'uni',
            }

    # Intentar match por patrones de Moodle
    result = find_brain_os_course(query)
    if result:
        return {
            'folder': result['local_folder'].split('/')[0],
            'notion_id': result['notion_id'],
            'type': 'personal' if result.get('is_personal') else 'uni',
        }
    return None

def call_mcp_tool(tool_name, arguments):
    """
    Calls an MCP tool via the standard input/output mechanism.
    In a real agent environment, this is mocked or handled by the agent context.
    For this script to run standalone, we might need a bridge. 
    However, since the Agent executes this, we will print a SPECIAL FORMAT 
    that the Agent can intercept if needed, OR we rely on the Agent 
    calling the MCP tool directly *after* this script returns the parameters.
    
    BUT, the request is for the script to do it. 
    Since I cannot easily call MCP from a python subprocess without the MCP client,
    I will output a JSON structure that the Agent can parse to make the call, 
    OR I will simulate it if I have the `mcp-client` library (which I don't).
    
    Strategy: This script provides the Logic. 
    The Agent (me) will run this script, capture the output (JSON), 
    and then perform the Notion API call myself.
    
    Wait, that's complex for the "Run and Forget" user experience.
    The user wants "Guarda este archivo".
    
    Alternative: I (The Agent) am the one executing the logic.
    I don't need this python script to call Notion. 
    I can use this script to MOVE the file, and return the Notion parameters.
    Then I call Notion.
    """
    pass

# =============================================================================
# MAIN LOGIC
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Ingest a file into Brain OS")
    parser.add_argument("--file", required=True, help="Path to the file")
    parser.add_argument("--course", required=True, help="Course key or partial name")
    parser.add_argument("--url", help="URL of the resource", default="")
    parser.add_argument("--title", help="Custom title for the resource (Notion Name)", default=None)
    
    args = parser.parse_args()
    
    file_path = args.file
    if not os.path.exists(file_path):
        print(json.dumps({"error": f"File not found: {file_path}"}))
        sys.exit(1)
        
    course_info = find_course(args.course)
    if not course_info:
        print(json.dumps({"error": f"Course not found for query: {args.course}"}))
        sys.exit(1)
        
    # Determine Destination
    if course_info['type'] == 'uni':
        base_folder = UNI_DIR
    else:
        base_folder = PERSONAL_DIR
        
    dest_dir = os.path.join(base_folder, course_info['folder'], "01_Materiales")
    
    # Create dir if not exists (safety)
    os.makedirs(dest_dir, exist_ok=True)
    
    filename = os.path.basename(file_path)
    dest_path = os.path.join(dest_dir, filename)
    
    # Move File
    try:
        shutil.move(file_path, dest_path)
    except Exception as e:
        print(json.dumps({"error": f"Failed to move file: {str(e)}"}))
        sys.exit(1)
        
    # Infer Type
    fname_upper = filename.upper()
    if "SILABO" in fname_upper or "SILABUS" in fname_upper:
        resource_type = "📄Silabo"
    elif filename.lower().endswith(('.ppt', '.pptx')):
        resource_type = "📊Ppt"
    else:
        resource_type = "📖 Libro" # Default for readings/others

    # Prepare URL/File Property
    url_property = []
    if args.url:
        url_property = [{
            "name": filename,
            "external": {"url": args.url}
        }]

    # Prepare Notion Data
    response = {
        "status": "success",
        "moved_to": dest_path,
        "notion_data": {
            "parent": {"database_id": NOTION_DB_RECURSOS},
            "properties": {
                "Nombre del recurso": {
                    "title": [{"text": {"content": args.title if args.title else filename}}]
                },
                "Tipo": {
                    "select": {"name": resource_type}
                },
                "Área Relacionada": {
                    "relation": [{"id": course_info['notion_id']}]
                },
                "Revisado": {
                    "checkbox": False
                },
                "Aporte": {
                    "select": {"name": "Aporte 1"}
                },
                "URL / Archivo": {
                    "files": url_property
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"text": {"content": "Archivo local: "}},
                            {"text": {"content": dest_path, "code": True}}
                        ]
                    }
                }
            ]
        }
    }
    
    print(json.dumps(response))

if __name__ == "__main__":
    main()
