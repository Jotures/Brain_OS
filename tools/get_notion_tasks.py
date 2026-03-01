import os
import requests
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment
# Assuming script is in tools/notion/ or similar, but we run from root usually?
# Let's try to find .env in current dir or parent
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

def get_pending_tasks():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    payload = {
        "filter": {
            "property": "Estado",
            "status": {
                "does_not_equal": "Listo"
            }
        },
        "sorts": [
            {
                "property": "Fecha Entrega",
                "direction": "ascending"
            }
        ]
    }
    
    resp = requests.post(url, headers=headers, json=payload)
    
    if resp.status_code != 200:
        print(f"Error: {resp.status_code} - {resp.text}")
        return []
        
    return resp.json().get("results", [])

def format_date(date_str):
    if not date_str: return "Sin fecha"
    try:
        dt = datetime.fromisoformat(date_str)
        # Weekday in Spanish
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        day_name = days[dt.weekday()]
        return f"{day_name} {dt.day}/{dt.month}"
    except:
        return date_str

def get_page_content(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return f"Error fetching blocks: {resp.status_code}"
    
    results = resp.json().get("results", [])
    content_lines = []
    
    if not results:
        return "[No blocks found on page]"

    for block in results:
        btype = block.get("type")
        # specific debugging
        # print(f"DEBUG: Found block type: {btype}") 
        
        text_content = ""
        
        # Expanded support
        if btype == "paragraph":
            rich_text = block.get("paragraph", {}).get("rich_text", [])
            text_content = "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "callout":
            rich_text = block.get("callout", {}).get("rich_text", [])
            text_content = "💡 " + "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "bulleted_list_item":
            rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
            text_content = "• " + "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "numbered_list_item":
            rich_text = block.get("numbered_list_item", {}).get("rich_text", [])
            text_content = "1. " + "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "to_do":
            rich_text = block.get("to_do", {}).get("rich_text", [])
            checked = "[x]" if block.get("to_do", {}).get("checked") else "[ ]"
            text_content = f"{checked} " + "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "heading_1":
            rich_text = block.get("heading_1", {}).get("rich_text", [])
            text_content = "# " + "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "heading_2":
            rich_text = block.get("heading_2", {}).get("rich_text", [])
            text_content = "## " + "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "heading_3":
            rich_text = block.get("heading_3", {}).get("rich_text", [])
            text_content = "### " + "".join([t.get("plain_text", "") for t in rich_text])
        elif btype == "quote":
            rich_text = block.get("quote", {}).get("rich_text", [])
            text_content = "> " + "".join([t.get("plain_text", "") for t in rich_text])
        else:
            text_content = f"[{btype} block]"

        if text_content.strip():
            content_lines.append(text_content)
    
    return "\n  ".join(content_lines) # Return all lines now

def main():
    tasks = get_pending_tasks()
    
    output = []
    if not tasks:
        output.append("No hay tareas pendientes.")
    else:
        output.append(f"Encontradas {len(tasks)} tareas pendientes:\n")
        for page in tasks:
            props = page["properties"]
            title = props.get("Tarea", {}).get("title", [{"plain_text": "Sin nombre"}])[0]["plain_text"]
            
            # Date
            date_obj = props.get("Fecha Entrega", {}).get("date")
            date_str = date_obj.get("start") if date_obj else None
            
            fmt_date = format_date(date_str)
            
            # Status
            status_obj = props.get("Estado", {}).get("status")
            status = status_obj.get("name", "Unknown") if status_obj else "Unknown"
            
            # Priority
            select_obj = props.get("Prioridad", {}).get("select")
            prio_name = select_obj.get("name", "") if select_obj else ""
            
        # Content / Description (from property)
        desc_prop = props.get("Descripción", {}).get("rich_text", [])
        description = "".join([t.get("plain_text", "") for t in desc_prop])
        
        # Aporte
        aporte = props.get("Aporte", {}).get("select", {}).get("name", "")
        
        output.append(f"• {title}")
        meta = [f"📅 {fmt_date}", status]
        if prio_name: meta.append(prio_name)
        if aporte: meta.append(aporte)
        
        output.append(f"  {' | '.join(meta)}")
        
        if description:
            output.append(f"  📝 {description}")
            
        output.append("-" * 20)

    final_output = "\n".join(output)
    print(final_output)
    with open("pending_tasks.txt", "w", encoding="utf-8") as f:
        f.write(final_output)

if __name__ == "__main__":
    main()
