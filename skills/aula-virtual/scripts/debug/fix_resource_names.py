#!/usr/bin/env python3
"""
Fix Resource Names in Notion
============================
Updates the "Nombre del recurso" property in Notion to match the Moodle Resource Name
instead of the filename.
"""

import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Import Moodle API
from moodle_api import MoodleAPI

# Load environment
script_dir = Path(__file__).parent
env_path = script_dir.parent / ".env"
load_dotenv(env_path)

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_map import NOTION_DB_RECURSOS

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID_RECURSOS = NOTION_DB_RECURSOS

def get_notion_pages():
    """Fetch all pages in the Resources Database."""
    print("🔍 Fetching Notion pages...")
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID_RECURSOS}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    pages = []
    has_more = True
    next_cursor = None
    
    # Payload for recursion
    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
             print(f"❌ Error Notion: {resp.text}")
             break
             
        data = resp.json()
        
        pages.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")
        
    print(f"✅ Found {len(pages)} pages in Notion.")
    return pages

def update_notion_title(page_id, new_title):
    """Update the title of a Notion page."""
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    payload = {
        "properties": {
            "Nombre del recurso": {
                "title": [{"text": {"content": new_title}}]
            }
        }
    }
    
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print(f"   ✅ Updated to: {new_title}")
        return True
    else:
        print(f"   ❌ Failed to update: {resp.text}")
        return False

def main():
    print("🚀 Fix Resource Names: Starting...")

    # 1. Connect to Moodle
    try:
        api = MoodleAPI()
        courses = api.get_courses()
    except Exception as e:
        print(f"❌ Moodle Error: {e}")
        return

    # Map: filename -> Moodle Resource Name
    resource_map = {}
    
    print("📚 Building Moodle Resource Map (Filename -> Title)...")
    for course in courses:
        try:
            contents = api.get_course_contents(course['id'])
            for section in contents:
                for module in section.get('modules', []):
                    if module.get('modname') == 'resource':
                        contents_info = module.get('contents', [])
                        if contents_info:
                            file_data = contents_info[0]
                            filename = file_data.get('filename') # Actual physical filename
                            moodle_name = module.get('name')     # The title shown in Moodle
                            
                            if filename and moodle_name:
                                resource_map[filename] = moodle_name
        except Exception as e:
            pass

    print(f"✅ Mapped {len(resource_map)} known resources.")

    # 2. Get Notion Pages
    notion_pages = get_notion_pages()
    
    updates_count = 0
    
    print("\n🔍 Scanning Notion for filename matches...")
    for page in notion_pages:
        props = page.get("properties", {})
        
        # Get Current Title
        title_prop = props.get("Nombre del recurso", {}).get("title", [])
        if not title_prop:
            continue
            
        current_title = title_prop[0].get("text", {}).get("content", "")
        
        # Check match
        if current_title in resource_map:
            new_title = resource_map[current_title]
            
            if new_title != current_title:
                print(f"🔄 Found match for '{current_title}' -> New Title: '{new_title}'")
                update_notion_title(page['id'], new_title)
                updates_count += 1
        else:
             # Debug info for unmatched
             # print(f"   No mapping for: {current_title}")
             pass

    print("\n" + "="*50)
    print(f"🏁 Process Complete. Updated {updates_count} pages.")

if __name__ == "__main__":
    main()
