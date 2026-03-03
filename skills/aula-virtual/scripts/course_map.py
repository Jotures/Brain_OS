#!/usr/bin/env python3
"""
Brain OS — Registry Central del Ecosistema
==========================================
Fuente única de verdad para IDs y configuración de todos los sistemas:
- Moodle UAndina (URL, patrones de cursos)
- Notion (IDs de bases de datos, IDs de áreas por curso)
- NotebookLM (URLs de notebooks por curso)
- Brain OS (carpetas locales, emojis, nombres)

Todos los scripts del ecosistema deben importar IDs desde aquí.
"""

# =============================================================================
# MOODLE — Configuración
# =============================================================================

MOODLE_URL = "https://campus.uandina.edu.pe"

# Nota mínima aprobatoria en escala vigesimal (sistema peruano)
NOTA_MINIMA_APROBATORIA = 13

# =============================================================================
# NOTION — Bases de Datos
# =============================================================================

NOTION_DB_TAREAS = "2cbaacd6-8210-803b-b9d9-d78fa3066b2a"    # BD_TAREAS_MAESTRAS
NOTION_DB_RECURSOS = "2cbaacd6-8210-80ea-9bff-d7aa9ffe3c41"  # BD_RECURSOS
NOTION_DB_AREAS = "2cbaacd6-8210-803e-8df2-d2d5b84232c2"     # BD_AREAS (Cursos)
NOTION_DB_TRACKER = "2cbaacd6-8210-8064-bd2e-c5eccf539edc"   # BD_TRACKER_DIARIO
NOTION_PAGE_STUDENT_OS = "2cbaacd6-8210-8026-8123-c3e2ea77b09e"

# =============================================================================
# MAPEO DE CURSOS (Moodle ↔ Brain OS ↔ Notion ↔ NotebookLM)
# =============================================================================

COURSE_MAP = {
    'economia_ambiental': {
        'name': 'Economía Ambiental',
        'emoji': '📗',
        'notion_id': '2fdaacd6-8210-81ae-bffe-f00d7ebaf358',
        'moodle_patterns': ['ECONOMIA AMBIENTAL', 'ECONOMÍA AMBIENTAL', 'ECON AMBIENT'],
        'local_folder': '01_economia_ambiental/01_Materiales',
        'notebooklm_url': 'https://notebooklm.google.com/notebook/3a62837e-ddff-4aac-b1ce-4847fd90e842',
    },
    'economia_internacional': {
        'name': 'Economía Internacional I',
        'emoji': '📘',
        'notion_id': '2fdaacd6-8210-8176-95da-f8f559269cc1',
        'moodle_patterns': ['ECONOMIA INTERNACIONAL', 'ECONOMÍA INTERNACIONAL', 'ECON INTER'],
        'local_folder': '02_economia_internacional/01_Materiales',
        'notebooklm_url': 'https://notebooklm.google.com/notebook/2efe8c43-6888-446f-803d-5f57a9485ecb',
    },
    'economia_gestion_publica': {
        'name': 'Economía y Gestión Pública',
        'emoji': '📙',
        'notion_id': '2fdaacd6-8210-81a1-91d1-ce49066ad036',
        'moodle_patterns': ['GESTION PUBLICA', 'GESTIÓN PÚBLICA', 'ECON GEST PUB'],
        'local_folder': '03_economia_gestion_publica/01_Materiales',
        'notebooklm_url': 'https://notebooklm.google.com/notebook/b62f9068-a5a0-4647-a9bb-2e7a15001d9d',
    },
    'investigacion_operativa': {
        'name': 'Investigación Operativa',
        'emoji': '📕',
        'notion_id': '2fdaacd6-8210-8133-9234-c6de69555825',
        'moodle_patterns': ['INVESTIGACION OPERATIVA', 'INVESTIGACIÓN OPERATIVA', 'INV OPER'],
        'local_folder': '04_investigacion_operativa/01_Materiales',
        'notebooklm_url': 'https://notebooklm.google.com/notebook/7dca47a9-fa22-438b-b05a-d4204ccf0242',
    },
    'teoria_monetaria': {
        'name': 'Teoría Monetaria y Bancaria',
        'emoji': '📔',
        'notion_id': '2fdaacd6-8210-8108-bb2a-ef7bba8a5825',
        'moodle_patterns': ['TEORIA MONETARIA', 'TEORÍA MONETARIA', 'MONETARIA Y BANCARIA'],
        'local_folder': '05_teoria_monetaria/01_Materiales',
        'notebooklm_url': 'https://notebooklm.google.com/notebook/db8832ff-e387-4345-8d91-891984ba8636',
    },
    'investigacion_economica': {
        'name': 'Investigación Económica',
        'emoji': '📓',
        'notion_id': '2fdaacd6-8210-8143-8a86-f17fd377fe70',
        'moodle_patterns': ['INVESTIGACION ECONOMICA', 'INVESTIGACIÓN ECONÓMICA', 'INV ECON'],
        'local_folder': '06_investigacion_economica/01_Materiales',
        'notebooklm_url': 'https://notebooklm.google.com/notebook/79852344-04fa-41ac-9988-b888d65f09a2',
    },
    'ingles': {
        'name': 'Inglés',
        'emoji': '📒',
        'notion_id': '2fdaacd6-8210-8134-aa64-df39374251ed',
        'moodle_patterns': ['INGLES', 'INGLÉS', 'ENGLISH'],
        'local_folder': 'ingles/01_Materiales',
        'notebooklm_url': 'https://notebooklm.google.com/notebook/c2607741-3ec8-4cd0-8fa5-5158712299b9',
        'is_personal': True,
    },
}


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
