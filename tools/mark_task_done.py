import os
import requests
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(".env")
if not env_path.exists():
    env_path = Path("skills/aula-virtual/.env")

if env_path.exists():
    load_dotenv(env_path)

NOTION_TOKEN = os.getenv('NOTION_TOKEN')

# Importar ID centralizado desde course_map.py
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "aula-virtual" / "scripts"))
from course_map import NOTION_DB_TAREAS
DATABASE_ID = NOTION_DB_TAREAS

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def find_task(query):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Tarea",
            "title": {
                "contains": query
            }
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    results = resp.json().get("results", [])
    return results

def mark_done(page_id, task_name):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Estado": {
                "status": {
                    "name": "Listo"
                }
            }
        }
    }
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print(f"✅ Tarea marcada como LISTO: {task_name}")
    else:
        print(f"❌ Error al actualizar: {resp.text}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python mark_task_done.py 'Nombre de la tarea'")
        return

    query = sys.argv[1]
    print(f"🔍 Buscando tarea: '{query}'...")
    
    tasks = find_task(query)
    
    if not tasks:
        print("❌ No se encontró ninguna tarea con ese nombre.")
        return
        
    if len(tasks) > 1:
        print(f"⚠️ Se encontraron {len(tasks)} tareas. Actualizando la primera:")
    
    target_task = tasks[0]
    task_id = target_task["id"]
    
    # Get exact name for confirmation
    props = target_task["properties"]
    title = props.get("Tarea", {}).get("title", [{"plain_text": "Sin nombre"}])[0]["plain_text"]
    
    mark_done(task_id, title)

if __name__ == "__main__":
    main()
