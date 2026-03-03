import json

def main():
    try:
        with open('c:/Users/Ruben J/Documents/Antigravito Proyects/Brain_OS/backups/tareas_latest.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            print(f"Total results in JSON: {len(data.get('results', []))}")
            for res in data.get('results', []):
                props = res.get('properties', {})
                name_prop = props.get('Nombre', {}).get('title', [])
                if name_prop:
                    name = name_prop[0].get('text', {}).get('content', '')
                    print(f"- {name} (ID: {res['id']})")
                else:
                    print(f"- [No Name] (ID: {res['id']})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
