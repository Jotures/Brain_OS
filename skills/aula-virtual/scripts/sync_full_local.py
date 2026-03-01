import requests
import os
import json
import mimetypes
from pathlib import Path
from dotenv import load_dotenv

# Load environment
script_dir = Path(__file__).parent
env_path = script_dir.parent / ".env"
load_dotenv(env_path)

from course_map import NOTION_DB_RECURSOS, NOTION_DB_AREAS, COURSE_MAP

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID_RECURSOS = NOTION_DB_RECURSOS
BASE_DIR = Path("c:/Users/Ruben J/Documents/Antigravito Proyects/Brain_OS/carrera/semestres/2026-1/cursos")

def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"

def upload_file_v1(filename, file_path):
    print(f"      🚀 Starting Upload for {filename}...")
    mime_type = get_mime_type(filename)
    file_size = os.path.getsize(file_path)

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # Step 1: Initialize
    init_url = "https://api.notion.com/v1/file_uploads"
    init_payload = {
        "name": filename,
        "content_type": mime_type,
        "content_length": file_size
    }
    
    try:
        init_resp = requests.post(init_url, headers=headers, json=init_payload)
        if init_resp.status_code != 200:
            print(f"      ❌ Init failed: {init_resp.text}")
            return None
        
        data = init_resp.json()
        file_upload_id = data.get("id")
        
        # Step 2: Send Bytes
        send_url = f"https://api.notion.com/v1/file_uploads/{file_upload_id}/send"
        
        with open(file_path, "rb") as f:
            headers_send = {
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": mime_type 
            }
            send_resp = requests.post(send_url, headers=headers_send, data=f.read())
            
            if send_resp.status_code == 200:
                print("      ✅ Upload Content success.")
                return file_upload_id
            else:
                # Retry Multipart
                f.seek(0)
                files = {'file': (filename, f, mime_type)}
                headers_multi = {"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": "2022-06-28"}
                send_resp_2 = requests.post(send_url, headers=headers_multi, files=files)
                if send_resp_2.status_code == 200:
                     print("      ✅ Upload Content success (Multipart).")
                     return file_upload_id
                else:
                     print(f"      ❌ Upload failed: {send_resp.text}")
                     return None
                     
    except Exception as e:
        print(f"      ❌ Exception: {e}")
        return None

def attach_file_v1(page_id, file_upload_id, filename):
    print(f"      ✨ Appending File Block...")
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    payload = {
        "children": [
            {
                "object": "block",
                "type": "file",
                "file": {
                    "type": "file_upload",
                    "file_upload": {"id": file_upload_id},
                    "caption": [{"type": "text", "text": {"content": filename}}]
                }
            }
        ]
    }
    
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        print("      ✅ Block Attached.")
        return True
    return False

# def clean_property(page_id, headers): -> Deprecated


def get_course_mapping():
    print("📚 Fetching Course Mapping...")
    COURSE_DB_ID = NOTION_DB_AREAS
    url = f"https://api.notion.com/v1/databases/{COURSE_DB_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    mapping = {}
    has_more = True
    next_cursor = None
    
    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        resp = requests.post(url, headers=headers, json=payload)
        data = resp.json()
        
        for page in data.get("results", []):
            try:
                # Assuming title property is "Nombre" or "Name" or similar.
                # Let's try "Nombre" based on standard conventions or inspect if it fails.
                # Actually, standard title is usually "Name" or "Nombre".
                # Let's inspect properties keys if needed, but for now guess "Nombre".
                props = page.get("properties", {})
                title_key = next((k for k, v in props.items() if v["id"] == "title"), None)
                if title_key:
                    title_list = props[title_key].get("title", [])
                    if title_list:
                        course_name = title_list[0]["plain_text"]
                        mapping[page["id"]] = course_name
            except Exception as e:
                pass
                
        has_more = data.get("has_more")
        next_cursor = data.get("next_cursor")
        
    print(f"✅ Mapped {len(mapping)} courses.")
    return mapping

def extract_url_from_shortcut(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith('URL='):
                    return line.strip().split('=', 1)[1]
    except:
        pass
    return None

def update_local_path(page_id, local_path, headers):
    print("   📍 Updating 'Ruta Local'...")
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Ruta Local": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": str(local_path)}
                    }
                ]
            }
        }
    }
    requests.patch(url, headers=headers, json=payload)

def create_resource_page(filename, course_id, headers, external_url=None):
    print(f"   ✨ Creating new page for: {filename}")
    url = "https://api.notion.com/v1/pages"
    
    # Infer Type
    res_type = "📄Lectura" # Default
    if filename.lower().endswith(".pptx"):
        res_type = "📊Ppt"
    elif filename.lower().endswith(".url"):
        res_type = "🔗 Link"
    
    # We need the Option ID for the select property if possible, or just name?
    # Notion API allows creating select by name usually.
    
    properties = {
            "Nombre del recurso": {
                "title": [{"text": {"content": filename.replace('.url', '')}}] # Clean name
            },
            "Área Relacionada": {
                "relation": [{"id": course_id}]
            },
            "Tipo": {
                "select": {"name": res_type}
            },
            # Force Aporte 1 as requested
            "Aporte": {
                "select": {"name": "Aporte 1"}
            },
            "Ruta Local": {
                "rich_text": [{"text": {"content": "Pending..."}}] 
            }
    }

    payload = {
        "parent": {"database_id": NOTION_DB_RECURSOS},
        "properties": properties
    }
    
    # If it's a URL type, we can add the link as a block OR if there is a URL property (which we decided not to use).
    # We will append the bookmark block LATER in the main loop if identified.
    # But wait, create_page can also take children.
    
    if external_url:
        payload["children"] = [
            {
                "object": "block",
                "type": "bookmark",
                "bookmark": {
                    "url": external_url
                }
            }
        ]
    
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        print(f"   ❌ Error creating page: {resp.text}")
        return None
    
    return resp.json()["id"]

    
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        print(f"   ❌ Error creating page: {resp.text}")
        return None
    
    return resp.json()["id"]

def main():
    print(f"📂 Scanning Local Directory: {BASE_DIR}")
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # ID -> Name
    course_map_id_to_name = get_course_mapping()
    # Name -> ID (Reverse map for creation)
    course_map_name_to_id = {v: k for k, v in course_map_id_to_name.items()}


    # Walk directory
    local_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith(('.pdf', '.pptx', '.docx', '.url')):
                full_path = Path(root) / file
                local_files.append(full_path)

    print(f"🔍 Found {len(local_files)} local files.")

    for file_path in local_files:
        filename = file_path.name
        is_url_shortcut = filename.lower().endswith('.url')
        clean_filename = filename.replace('.url', '') if is_url_shortcut else filename
        
        print(f"\n📦 Check: {clean_filename}")
        
        # Determine expected course from path
        parent_folder = file_path.parent.parent.name 
        
        expected_course_id = None
        expected_course_name = ""
        target_course_id = None
        
        # Determine course info from local folder path using COURSE_MAP
        for c_key, c_info in COURSE_MAP.items():
             if c_info.get('local_folder', '').split('/')[0] in str(file_path):
                 expected_course_name = c_info['name']
                 target_course_id = c_info['notion_id'].replace("-", "") # Ensure dash-less ID formatting for Notion API
                 expected_course_id = c_info['notion_id']
                 break
        
        print(f"   🎯 Expected Course: {expected_course_name}")

        # 1. Search Notion
        query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID_RECURSOS}/query"
        payload = {"filter": {"property": "Nombre del recurso", "title": {"contains": clean_filename}}} 
        
        resp = requests.post(query_url, headers=headers, json=payload)
        results = resp.json().get("results", [])
        
        if not results:
            print("   ⚠️ Page not found in Notion.")
            
            # Auto-Create Logic
            print("   💡 Attempting to create page...")
            
            if target_course_id:
                # Extract URL if valid
                external_url = None
                if is_url_shortcut:
                     external_url = extract_url_from_shortcut(file_path)

                new_page_id = create_resource_page(filename, target_course_id, headers, external_url)
                if new_page_id:
                    # Treat as a 'result' to process below
                    print(f"   ✅ Created page ID: {new_page_id}")
                    results = [{"id": new_page_id, "properties": {"Nombre del recurso": {"title": [{"plain_text": clean_filename}]}}}]
                else:
                    continue
            else:
                print(f"   ❌ Could not find Course ID for '{expected_course_name}'. Skipping creation.")
                continue
            
        for page in results:
            page_id = page["id"]
            page_title = clean_filename 

            if "properties" in page and "Nombre del recurso" in page["properties"]:
                 try:
                     page_title = page["properties"]["Nombre del recurso"]["title"][0]["plain_text"]
                 except: pass

            # Validation: Check Area Relacionada (Course)
            # If we just created it, we know it's valid.
            # If it's existing, we validate and auto-correct.
            
            if "properties" in page and "Área Relacionada" in page["properties"]:
                relation = page["properties"].get("Área Relacionada", {}).get("relation", [])
                is_valid_course = False
                
                if not relation:
                    print("   ⚠️ No linked course. Auto-correcting...")
                else:
                    for rel in relation:
                        rel_id = rel["id"].replace("-", "")
                        # Compare against our known target_course_id from COURSE_MAP
                        if target_course_id and rel_id == target_course_id:
                            is_valid_course = True
                            break
                
                if not is_valid_course and target_course_id:
                     print(f"   🔄 Fixing Course Mismatch for '{page_title}' -> setting to {expected_course_name}")
                     # Auto-correct logic
                     patch_url = f"https://api.notion.com/v1/pages/{page_id}"
                     patch_payload = {
                         "properties": {
                             "Área Relacionada": {
                                 "relation": [{"id": expected_course_id}]
                             }
                         }
                     }
                     requests.patch(patch_url, headers=headers, json=patch_payload)
            else:
                # Needed for the mocked object case
                pass

            print(f"   ✅ Match confirmed for: {page_title}")

            
            # 2. Update Local Path
            update_local_path(page_id, file_path, headers)
            
            # 3. Deduplication & Upload
            blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            blocks_resp = requests.get(blocks_url, headers=headers)
            blocks = blocks_resp.json().get("results", [])
            
            existing_file_blocks = []
            for b in blocks:
                if b.get("type") == "file":
                    caption = b.get("file", {}).get("caption", [])
                    if caption and caption[0].get("text", {}).get("content") == filename:
                        existing_file_blocks.append(b)
            
            if len(existing_file_blocks) > 0:
                print("   ✅ File already uploaded.")
                # Cleanup duplicates
                if len(existing_file_blocks) > 1:
                    for b_rem in existing_file_blocks[:-1]:
                        requests.delete(f"https://api.notion.com/v1/blocks/{b_rem['id']}", headers=headers)
                    print("      🧹 Duplicates removed.")
            else:
                # Upload
                f_id = upload_file_v1(filename, str(file_path))
                if f_id:
                        attach_file_v1(page_id, f_id, filename)
            
            # 4. Property Cleanup - REMOVED (Property deleted by user)
            # clean_property(page_id, headers)

if __name__ == "__main__":
    main()
