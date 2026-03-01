import json

def parse():
    try:
        with open(r"C:\Users\Ruben J\.gemini\antigravity\brain\cc41bc12-048b-4471-a85e-b342fa5af412\.system_generated\steps\75\output.txt", 'r', encoding='utf-8') as f:
            data = json.load(f)
        results = data.get('results', [])
        for item in results:
            obj = item.get('object', '')
            title_arr = item.get('title', []) if obj == 'database' else item.get('properties', {}).get('title', {}).get('title', [])
            title = 'No title'
            if title_arr:
                title = title_arr[0].get('plain_text', '')
            print(f"[{obj}] Title: {title} | ID: {item.get('id')}")
    except Exception as e:
        print(f"Error parsing json: {e}")

if __name__ == '__main__':
    parse()
