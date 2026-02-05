#!/usr/bin/env python3
"""
Mapeo de Cursos: Moodle UAndina ↔ Brain OS ↔ Notion
===================================================
Define la correlación entre IDs de cursos en diferentes sistemas.

Este mapeo permite:
1. Identificar a qué curso Brain OS pertenece una tarea de Moodle
2. Crear tareas en Notion bajo el área correcta
3. Filtrar tareas por curso usando nombres amigables
"""

# =============================================================================
# MAPEO DE CURSOS
# =============================================================================
# 
# Estructura:
#   brain_os_id: {
#       'name': Nombre amigable para mostrar
#       'emoji': Emoji del curso
#       'notion_id': ID de la página del curso en Notion (BD_AREAS)
#       'moodle_patterns': Patrones para identificar el curso en Moodle
#   }

COURSE_MAP = {
    'economia_ambiental': {
        'name': 'Economía Ambiental',
        'emoji': '📗',
        'notion_id': '2fdaacd6-8210-81ae-bffe-f00d7ebaf358',
        'moodle_patterns': ['ECONOMIA AMBIENTAL', 'ECONOMÍA AMBIENTAL', 'ECON AMBIENT'],
    },
    'economia_internacional': {
        'name': 'Economía Internacional I',
        'emoji': '📘',
        'notion_id': '2fdaacd6-8210-8176-95da-f8f559269cc1',
        'moodle_patterns': ['ECONOMIA INTERNACIONAL', 'ECONOMÍA INTERNACIONAL', 'ECON INTER'],
    },
    'economia_gestion_publica': {
        'name': 'Economía y Gestión Pública',
        'emoji': '📙',
        'notion_id': '2fdaacd6-8210-81a1-91d1-ce49066ad036',
        'moodle_patterns': ['GESTION PUBLICA', 'GESTIÓN PÚBLICA', 'ECON GEST PUB'],
    },
    'investigacion_operativa': {
        'name': 'Investigación Operativa',
        'emoji': '📕',
        'notion_id': '2fdaacd6-8210-8133-9234-c6de69555825',
        'moodle_patterns': ['INVESTIGACION OPERATIVA', 'INVESTIGACIÓN OPERATIVA', 'INV OPER'],
    },
    'teoria_monetaria': {
        'name': 'Teoría Monetaria y Bancaria',
        'emoji': '📔',
        'notion_id': '2fdaacd6-8210-8108-bb2a-ef7bba8a5825',
        'moodle_patterns': ['TEORIA MONETARIA', 'TEORÍA MONETARIA', 'MONETARIA Y BANCARIA'],
    },
    'investigacion_economica': {
        'name': 'Investigación Económica',
        'emoji': '📓',
        'notion_id': '2fdaacd6-8210-8143-8a86-f17fd377fe70',
        'moodle_patterns': ['INVESTIGACION ECONOMICA', 'INVESTIGACIÓN ECONÓMICA', 'INV ECON'],
    },
    'ingles': {
        'name': 'Inglés',
        'emoji': '📒',
        'notion_id': '2fdaacd6-8210-8134-aa64-df39374251ed',
        'moodle_patterns': ['INGLES', 'INGLÉS', 'ENGLISH'],
        'is_personal': True,  # Curso personal, no universitario
    },
}

# ID de la base de datos de tareas en Notion
NOTION_DB_TAREAS = "2cbaacd6-8210-803b-b9d9-d78fa3066b2a"  # BD_TAREAS_MAESTRAS correcto


def find_brain_os_course(moodle_course_name: str) -> dict | None:
    """
    Encuentra el curso Brain OS correspondiente a un nombre de Moodle.
    
    Args:
        moodle_course_name: Nombre del curso como aparece en Moodle
        
    Returns:
        Diccionario con info del curso o None si no hay match
    """
    moodle_upper = moodle_course_name.upper()
    
    for course_id, course_info in COURSE_MAP.items():
        for pattern in course_info['moodle_patterns']:
            if pattern.upper() in moodle_upper:
                return {
                    'id': course_id,
                    **course_info
                }
    
    return None


def get_all_courses() -> list:
    """Retorna lista de todos los cursos configurados."""
    return [
        {'id': cid, **cinfo}
        for cid, cinfo in COURSE_MAP.items()
    ]


if __name__ == "__main__":
    # Test del mapeo
    test_names = [
        "PRE-P-20261-CUSCO-ECONOMÍA-TEORÍA MONETARIA Y BANCARIA-7B",
        "ECONOMIA AMBIENTAL-7B",
        "INVESTIGACION OPERATIVA 2026-1",
    ]
    
    print("🔄 Test de Mapeo de Cursos")
    print("=" * 50)
    
    for name in test_names:
        result = find_brain_os_course(name)
        if result:
            print(f"✅ {name[:40]}...")
            print(f"   → {result['emoji']} {result['name']}")
            print(f"   → Notion: {result['notion_id'][:8]}...")
        else:
            print(f"❌ {name[:40]}... → No match")
        print()
