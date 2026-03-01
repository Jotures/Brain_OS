from skills.aula_virtual.scripts.moodle_api import MoodleAPI
import json

def get_task_details():
    try:
        api = MoodleAPI()
        assignments = api.get_assignments()
        
        target_name = "La ventaja comparativa"
        
        for course in assignments.get('courses', []):
            for assignment in course.get('assignments', []):
                if target_name.lower() in assignment.get('name', '').lower():
                    print(f"FOUND_TASK_DETAILS")
                    print(f"Title: {assignment.get('name')}")
                    print(f"Due Date: {assignment.get('duedate')}")
                    print(f"Description: {assignment.get('intro')}")
                    print(f"Intro Attachments: {assignment.get('introattachments')}")
                    return
        
        print("Task not found in assignments.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_task_details()
