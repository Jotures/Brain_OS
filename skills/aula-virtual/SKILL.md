---
name: aula-virtual
description: Integración con el Aula Virtual de la Universidad Andina del Cusco (Moodle). Usa esta skill para consultar cursos, tareas pendientes, notas y materiales del campus virtual. Se activa cuando el usuario menciona "aula virtual", "campus", "moodle", "tareas pendientes", "mis notas", o cualquier referencia a la plataforma académica de UAndina.
---

# Aula Virtual UAndina

Integración con el campus virtual de la Universidad Andina del Cusco (campus.uandina.edu.pe).

## Configuración Inicial (Primera Vez)

### 1. Crear archivo .env
```bash
# En skills/aula-virtual/
cp .env.example .env
# Editar .env con tus credenciales
```

### 2. Obtener Token
```bash
cd skills/aula-virtual
pip install -r requirements.txt
python scripts/get_uandina_token.py
```

El token se guardará automáticamente en `.env`.

## Comandos Disponibles

| Di esto... | Brain OS hace... |
|------------|------------------|
| "¿Qué tareas tengo pendientes?" | Lista deadlines de Moodle |
| "Tareas de [curso]" | Filtra por curso específico |
| "Mis notas de [curso]" | Consulta calificaciones |
| "Cursos del aula virtual" | Lista cursos matriculados |
| "Sync aula virtual" | Sincroniza tareas a Notion |

## Uso Programático

```python
from scripts.moodle_api import MoodleAPI

# Inicializar (usa token de .env)
api = MoodleAPI()

# Obtener cursos
cursos = api.get_courses()

# Obtener deadlines próximos (14 días)
deadlines = api.get_upcoming_deadlines(14)

# Obtener notas de un curso
notas = api.get_grades(course_id=12345)
```

## Flujo de Sincronización

```
1. get_upcoming_deadlines() → Lista tareas con fechas
2. Mapear curso Moodle → curso Brain OS
3. Crear tareas en Notion (BD_TAREAS_MAESTRAS)
4. Actualizar INICIO.md (via dashboard-sync)
```

## Mapeo de Cursos

| Curso Moodle | Curso Brain OS | Notion ID |
|--------------|----------------|-----------|
| ECONOMIA AMBIENTAL | economia_ambiental | CURSO_ECONOMIA_AMBIENTAL |
| ECONOMIA INTERNACIONAL I | economia_internacional | CURSO_ECONOMIA_INTERNACIONAL |
| ... | ... | ... |

## Scripts Disponibles

| Script | Función |
|--------|---------|
| `get_uandina_token.py` | Obtiene y guarda el token de autenticación |
| `get_tasks.py` | 🦅 "Ojos de Águila" - Busca tareas en Moodle |
| `read_notion_tasks.py` | 📥 Lee tareas de BD_TAREAS_MAESTRAS |
| `course_map.py` | 🗺️ Mapeo cursos Moodle ↔ Brain OS ↔ Notion |
| `sync_to_notion.py` | 📤 Sincroniza tareas a BD_TAREAS_MAESTRAS |
| `moodle_client.py` | Cliente simple para probar conexión |
| `moodle_api.py` | API completa (cursos, tareas, notas) |

## Flujo Bidireccional

```
LECTURA:                          ESCRITURA:
Notion → read_notion_tasks.py     get_tasks.py → sync_to_notion.py → Notion
         ↓                                                            ↑
    Brain OS ←────────────────────────────────────────────────────────┘
```

## Notas de Seguridad

- **NUNCA** subir `.env` a git (ya está en .gitignore)
- El token expira, ejecutar `get_uandina_token.py` si hay errores de auth
- Solo funciona dentro de la red o con VPN de UAndina para algunos servicios

## Troubleshooting

| Error | Solución |
|-------|----------|
| "Invalid token" | Ejecutar `get_uandina_token.py` |
| "Service unavailable" | Verificar que usas `moodle_mobile_app` como servicio |
| "Connection error" | Verificar internet/VPN |
