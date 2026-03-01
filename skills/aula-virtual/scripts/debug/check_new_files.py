from moodle_api import MoodleAPI
import datetime
import time

def check_new_files():
    print("🔍 Mostrando archivos del Aula Virtual (Semestre 2026-1)...")
    print("-" * 50)
    
    try:
        api = MoodleAPI()
        courses = api.get_courses()
        
        found_files = 0
        
        for course in courses:
            course_name = course.get('fullname')
            course_id = course.get('id')
            
            # Skip if not current semester (optional filter, but let's check all enrolled)
            if "20261" not in course_name and "2026-1" not in course_name:
                 # Just a heuristic, maybe remove if user has weird course names
                 pass

            print(f"\n📂 Curso: {course_name}")
            
            contents = api.get_course_contents(course_id)
            
            for section in contents:
                section_name = section.get('name', 'General')
                modules = section.get('modules', [])
                
                for module in modules:
                    mod_name = module.get('name')
                    mod_type = module.get('modname')
                    
                    if mod_type == 'resource':
                        contents_list = module.get('contents', [])
                        for content in contents_list:
                            if content.get('type') == 'file':
                                filename = content.get('filename')
                                fileurl = content.get('fileurl')
                                timecreated = content.get('timecreated', 0)
                                date_str = datetime.datetime.fromtimestamp(timecreated).strftime('%Y-%m-%d')
                                
                                # Check if it's recent (e.g., last 30 days) or just list all for now
                                print(f"   📄 [{date_str}] {filename}")
                                found_files += 1

                    elif mod_type == 'folder':
                        contents_list = module.get('contents', [])
                        for content in contents_list:
                             if content.get('type') == 'file':
                                filename = content.get('filename')
                                date_str = datetime.datetime.fromtimestamp(content.get('timecreated', 0)).strftime('%Y-%m-%d')
                                print(f"   zj [{date_str}] {filename} (en carpeta '{mod_name}')")
                                found_files += 1
                                
        print("-" * 50)
        print(f"Total archivos encontrados: {found_files}")

    except Exception as e:
        print(f"❌ Error al escanear: {e}")

if __name__ == "__main__":
    check_new_files()
