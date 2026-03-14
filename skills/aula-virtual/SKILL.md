---
name: aula-virtual
description: Integración con el Aula Virtual de la Universidad Andina del Cusco (Moodle). Usa esta skill para consultar cursos, tareas pendientes, notas, progreso, materiales y preparación pre-examen. Se activa cuando el usuario menciona "aula virtual", "campus", "moodle", "tareas pendientes", "mis notas", "progreso", o cualquier referencia a la plataforma académica de UAndina.
trigger_conditions:
  - "Tareas pendientes del aula virtual"
  - "Mis notas en [curso]"
  - "Progreso del semestre"
  - "Materiales de [curso]"
  - "Preparación pre-examen desde Moodle"
  - "¿Qué tengo pendiente en el campus?"
usage_constraints: "Solo para la plataforma Moodle de UAndina (campus.uandina.edu.pe). No usar para consultas académicas generales (usar research-engineer o notebooklm). Requiere credenciales en .env."
category: "Académico"
parameters:
  course: "Nombre del curso (string, opcional)"
  action: "Operación: tasks | grades | progress | materials | exam-prep (inferido del comando)"
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
| "¿Qué tareas tengo pendientes?" | Lista deadlines con prioridad inteligente |
| "Tareas de [curso]" | Filtra por curso específico |
| "Mis notas" / "¿Cómo voy?" | Dashboard de calificaciones |
| "Mis notas --brief" | Resumen rápido de notas (boot matutino) |
| "Progreso de actividades" | Barra de progreso por curso |
| "Progreso de [curso]" | Progreso filtrado por curso |
| "Reporte semanal" | Reporte de rendimiento con tendencias |
| "Cursos del aula virtual" | Lista cursos matriculados |
| "Sync aula virtual" | Sincroniza tareas + calendario a Notion |
| "Hay materiales nuevos?" | Detecta archivos subidos recientemente |
| "¿Tengo exámenes pronto?" | Detector de evaluaciones próximas |
| "Preparar examen de [curso]" | Modo pre-examen inteligente |

## Scripts Disponibles

| Script | Función |
|--------|---------|
| `get_uandina_token.py` | Obtiene y guarda el token de autenticación |
| `get_tasks.py` | 🦅 "Ojos de Águila" v2 — Tareas con prioridad inteligente |
| `get_grades.py` | 📊 Dashboard de calificaciones en tiempo real |
| `get_progress.py` | 📋 Tracker de progreso de actividades |
| `weekly_report.py` | 📈 Reporte semanal de rendimiento con tendencias |
| `watch_materials.py` | 👁️ Watcher de materiales nuevos |
| `exam_detector.py` | 🔍 Detector de exámenes próximos |
| `pre_exam_orchestrator.py` | 🎯 Orquestador de modo pre-examen |
| `sync_assignments.py` | 📤 Sync tareas + calendario → Notion |
| `sync_full_local.py` | 📁 Sync archivos locales → Notion |
| `download_files.py` | 📥 Descarga archivos del aula virtual |
| `course_map.py` | 🗺️ Registry central de cursos |
| `moodle_api.py` | API completa (cursos, tareas, notas, progreso, calendario) |

## Uso Programático

```python
from scripts.moodle_api import MoodleAPI

api = MoodleAPI()

# Cursos, tareas, notas
cursos = api.get_courses()
deadlines = api.get_upcoming_deadlines(14)
notas = api.get_grades(course_id=12345)

# Progreso y calendario
progreso = api.get_course_progress_summary(course_id=12345)
eventos = api.get_upcoming_events(days=30)
actividades = api.get_activity_completion(course_id=12345)
```

## Flujo de Sincronización

```
1. Moodle → get_tasks.py → Prioridad inteligente (peso + tiempo)
2. Moodle → sync_assignments.py → Notion BD_TAREAS_MAESTRAS + Calendario
3. Moodle → download_files.py → Archivos Locales + .url
4. Archivos → sync_full_local.py → Notion BD_RECURSOS
5. Moodle → watch_materials.py → Detecta nuevos archivos
```

## Sistema de Prioridad Inteligente

Fórmula: `urgencia = (peso_en_nota × 0.4) + (factor_tiempo × 0.6)`

| Urgencia | Prioridad | Notion |
|----------|-----------|--------|
| ≥ 0.5 o ≤ 2 días | 🔥 Alta | `🔥 Alta` |
| ≥ 0.25 o ≤ 7 días | ⚡ Media | `⚡ Media` |
| < 0.25 | ☁️ Baja | `☁️ Baja` |

## Modo Pre-Examen 🎯

Cuando se detecta un examen próximo, el orquestador genera configuración para:

| Componente | Acción |
|------------|--------|
| **Pomodoro** | Perfil `exam_prep` (45min/8min) o `intensive` |
| **Active Recall** | Intensidad alta, 5-7 preguntas/sesión, Bloom 4-5 |
| **NotebookLM** | URL del notebook del curso para consulta |
| **Estrategia** | Personalizada según días restantes |

```bash
# Detectar exámenes
python scripts/exam_detector.py --days 14

# Generar config pre-examen
python scripts/pre_exam_orchestrator.py --course "Investigación Operativa"
python scripts/pre_exam_orchestrator.py --all --json
```

## Mapeo de Cursos

| Curso Moodle | Curso Brain OS | Notion ID |
|--------------|----------------|-----------|
| ECONOMIA AMBIENTAL | economia_ambiental | CURSO_ECONOMIA_AMBIENTAL |
| ECONOMIA INTERNACIONAL I | economia_internacional | CURSO_ECONOMIA_INTERNACIONAL |
| ... | ... | ... |

Ver `course_map.py` para el mapeo completo.

## Notas de Seguridad

- **NUNCA** subir `.env` a git (ya está en .gitignore)
- El token expira, ejecutar `get_uandina_token.py` si hay errores de auth
- Solo funciona dentro de la red o con VPN de UAndina para algunos servicios

## Troubleshooting

| Error | Solución |
|-------|----------|
| "Invalid token" | Ejecutar `get_uandina_token.py` |
| "Service unavailable" | Verificar servicio `moodle_mobile_app` |
| "Connection error" | Verificar internet/VPN |
| "No grades found" | El profesor aún no ha publicado notas |
| "No completion tracking" | El curso no tiene tracking habilitado en Moodle |
