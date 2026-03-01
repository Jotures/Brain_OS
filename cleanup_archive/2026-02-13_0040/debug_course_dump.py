from moodle_api import MoodleAPI
import json

def dump_course():
    api = MoodleAPI()
    print("🔍 Fetching courses...")
    courses = api.get_courses()
    
    target_course = None
    for c in courses:
        if "INVESTIGACION" in c.get("fullname", "").upper() and "ECONOMICA" in c.get("fullname", "").upper():
            target_course = c
            break
            
    if not target_course:
        print("❌ 'Investigación Económica' course not found.")
        return

    print(f"🎯 Found Course: {target_course['fullname']} (ID: {target_course['id']})")
    
    print("📥 Fetching contents...")
    contents = api.get_course_contents(target_course['id'])
    
    # Dump full JSON to file for inspection
    with open("debug_course_dump.json", "w", encoding="utf-8") as f:
        json.dump(contents, f, indent=4, ensure_ascii=False)
        
    print("✅ Dump saved to debug_course_dump.json")
    
    # Print summary of modules in 'Unidad 1'
    for section in contents:
        print(f"\n📂 Section: {section.get('name')}")
        for mod in section.get('modules', []):
            print(f"   - [{mod.get('modname')}] {mod.get('name')} (ID: {mod.get('id')})")
            if mod.get('modname') == 'url':
                 print(f"     -> URL: {mod.get('contents', [{}])[0].get('fileurl', 'N/A')}")
            if "LECTURA" in mod.get('name', '').upper():
                 print(f"     🚨 FOUND THE TARGET! Type is: {mod.get('modname')}")

if __name__ == "__main__":
    dump_course()
