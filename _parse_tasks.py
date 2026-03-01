import json
import sys
from datetime import datetime

def parse(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        results = data.get('results', [])
        
        pending_tasks = []
        for item in results:
            props = item.get('properties', {})
            
            # Extract name
            name_prop = props.get('Tarea', {}) or props.get('Name', {})
            name = "[Untitled]"
            for k, v in props.items():
                if v.get('type') == 'title' and v.get('title'):
                    name = v['title'][0].get('plain_text', '')
                    break
            
            # Extract state
            state = ""
            for k, v in props.items():
                if v.get('type') == 'status' and v.get('status'):
                    state = v['status'].get('name', '')
                elif v.get('type') == 'select' and k == 'Estado':
                    state = v['select'].get('name', '')
                if state: break
                
            # Extract Date
            date = ""
            for k, v in props.items():
                if v.get('type') == 'date' and v.get('date'):
                    date = v['date'].get('start', '')
                    break
                    
            if state.lower() != 'listo':
                pending_tasks.append({'name': name, 'state': state, 'date': date})
                
        # Sort by date
        def get_date(task):
            return task['date'] if task['date'] else '9999-12-31'
            
        pending_tasks.sort(key=get_date)
                
        print(f"Pending tasks: {len(pending_tasks)}")
        for i, t in enumerate(pending_tasks):
            print(f"{i+1}. {t['name']} (Deadline: {t['date']}) - {t['state']}")
            
    except Exception as e:
        print(f"Error parsing json: {e}")

if __name__ == '__main__':
    parse(sys.argv[1])
