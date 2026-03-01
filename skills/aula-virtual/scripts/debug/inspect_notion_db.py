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

def inspect_db():
    print(f"🔍 Inspecting Database: {DATABASE_ID}")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    has_more = True
    next_cursor = None
    all_pages = []

    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            print(f"❌ Error: {resp.text}")
            break
            
        data = resp.json()
        all_pages.extend(data.get("results", []))
        has_more = data.get("has_more")
        next_cursor = data.get("next_cursor")

    print(f"✅ Found {len(all_pages)} pages in Notion.")
    
    print("\n📊 Detailed Report:")
    print(f"{'NAME':<60} | {'PROP_URL':<10} | {'BLOCKS'}")
    print("-" * 100)
    
    for page in all_pages:
        page_id = page["id"]
        props = page.get("properties", {})
        
        # Name
        title_prop = props.get("Nombre del recurso", {}).get("title", [])
        name = title_prop[0].get("plain_text") if title_prop else "[No Name]"
        
        # Property URL
        url_files = props.get("URL / Archivo", {}).get("files", [])
        has_prop_url = "YES" if url_files else "NO"
        
        # Blocks (Check for File/PDF blocks)
        blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        b_resp = requests.get(blocks_url, headers=headers)
        blocks = b_resp.json().get("results", [])
        
        file_blocks = 0
        for b in blocks:
            if b.get("type") in ["file", "pdf", "image"]:
                file_blocks += 1
                
        print(f"{name[:58]:<60} | {has_prop_url:<10} | {file_blocks} native blocks")

if __name__ == "__main__":
    inspect_db()
