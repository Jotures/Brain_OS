import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

script_dir = Path(__file__).parent
env_path = script_dir.parent / ".env"
load_dotenv(env_path)

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_map import NOTION_DB_RECURSOS

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = NOTION_DB_RECURSOS

def add_property():
    print(f"🔧 Updating Schema for Database: {DATABASE_ID}")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # Payload to add a property
    payload = {
        "properties": {
            "Ruta Local": {
                "rich_text": {}
            }
        }
    }
    
    resp = requests.patch(url, headers=headers, json=payload)
    
    if resp.status_code == 200:
        print("✅ Property 'Ruta Local' added successfully!")
    else:
        print(f"❌ Failed to add property: {resp.text}")

if __name__ == "__main__":
    add_property()
