import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

script_dir = Path(__file__).parent
env_path = script_dir.parent / ".env"
load_dotenv(env_path)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "2cbaacd6-8210-80ea-9bff-d7aa9ffe3c41"

def debug_resource(filename):
    print(f"🔍 Searching for: {filename}")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # Try exact match first
    payload = {"filter": {"property": "Nombre del recurso", "title": {"equals": filename}}}
    resp = requests.post(url, headers=headers, json=payload)
    results = resp.json().get("results", [])
    
    if not results:
        print("   ❌ Exact match not found. Trying 'contains'...")
        payload = {"filter": {"property": "Nombre del recurso", "title": {"contains": filename}}}
        resp = requests.post(url, headers=headers, json=payload)
        results = resp.json().get("results", [])
    
    if not results:
        print("   ❌ Still not found.")
        return

    page = results[0]
    page_id = page["id"]
    print(f"   ✅ Found Page ID: {page_id}")
    
    # Check Properties
    props = page.get("properties", {})
    url_prop = props.get("URL / Archivo", {}).get("files", [])
    print(f"   📂 Property 'URL / Archivo': {len(url_prop)} items")
    for f in url_prop:
        print(f"      - Type: {f.get('type')} | Name: {f.get('name')} | URL: {f.get('external', {}).get('url')}")
        
    # Check Blocks
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    blocks_resp = requests.get(blocks_url, headers=headers)
    blocks = blocks_resp.json().get("results", [])
    
    print(f"   🧱 Blocks: {len(blocks)} items")
    for b in blocks:
        btype = b.get("type")
        if btype == "file":
             print(f"      - SYSTEM FILE BLOCK: {b.get('file', {}).get('caption', [{}])[0].get('text', {}).get('content', 'No Caption')}")
        elif btype == "pdf":
             print(f"      - PDF BLOCK: {b.get('pdf', {}).get('caption', [{}])[0].get('text', {}).get('content', 'No Caption')}")
        else:
             print(f"      - {btype}")

if __name__ == "__main__":
    debug_resource("sesion 2.pptx")
