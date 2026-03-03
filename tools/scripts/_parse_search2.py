import json

def parse_search_results():
    try:
        with open(r'C:\Users\Ruben J\.gemini\antigravity\brain\cc41bc12-048b-4471-a85e-b342fa5af412\.system_generated\steps\362\output.txt', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get('results', []):
                obj_type = item.get('object', '')
                obj_id = item.get('id', '')
                
                title = ""
                if obj_type == 'page':
                    props = item.get('properties', {})
                    for prop_name, prop_val in props.items():
                        if prop_val.get('type') == 'title':
                            title_arr = prop_val.get('title', [])
                            if title_arr:
                                title = title_arr[0].get('plain_text', '')
                
                if title:
                    print(f"[{obj_type}] ID: {obj_id} | Title: {title}")
    except Exception as e:
        print(f"Error parsing: {e}")

if __name__ == '__main__':
    parse_search_results()
