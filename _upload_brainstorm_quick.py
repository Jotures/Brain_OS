import os
import requests
from dotenv import load_dotenv

load_dotenv('skills/aula-virtual/.env')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
PAGE_ID = "315aacd6-8210-803a-acbf-cdef1e62cd99"
FILE_PATH = r"C:\Users\Ruben J\.gemini\antigravity\brain\cc41bc12-048b-4471-a85e-b342fa5af412\brainstorming_eco_int.md"

def upload_markdown():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content into chunks of 1900 chars to avoid Notion limits safely
    chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
    
    children = []
    children.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "🧠 Resultado de Brainstorming (Brain OS)"}}]
        }
    })
    
    for chunk in chunks:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            }
        })

    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    print("Uploading to Notion...")
    resp = requests.patch(url, headers=headers, json={"children": children})
    if resp.status_code == 200:
        print("✅ Correctamente adjuntado a la tarea en Notion!")
    else:
        print(f"❌ Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    upload_markdown()
