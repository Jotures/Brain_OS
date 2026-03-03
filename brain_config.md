# 🧠 Brain OS - Archivo de Configuración

Archivo central con IDs y esquemas para la integración Notion MCP.

---

## Bases de Datos - IDs

```yaml
# Página Principal STUDENT OS
STUDENT_OS_PAGE: "2cbaacd6-8210-8026-8123-c3e2ea77b09e"

# Bases de Datos Master (en página BASES DE DATOS)
BD_AREAS: "2cbaacd6-8210-803e-8df2-d2d5b84232c2"
BD_TAREAS_MAESTRAS: "2cbaacd6-8210-803b-b9d9-d78fa3066b2a"
BD_RECURSOS: "2cbaacd6-8210-80ea-9bff-d7aa9ffe3c41"

# Vistas en Página Principal
DB_SEMESTRE: "2d3aacd6-8210-8077-9c39-fb3604600f64"
DB_EN_FOCO: "2d3aacd6-8210-80dd-8f84-c63c7192992e"
DB_RACHA: "2cbaacd6-8210-807b-8e7b-f39c0655b059"
```

---

## Esquema BD_TAREAS_MAESTRAS

### Propiedades
| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `Tarea` | title | Nombre de la tarea |
| `Estado` | status | Por hacer / En progreso / Listo |
| `Prioridad` | select | 🔥 Alta / ⚡ Media / ☁️ Baja |
| `Tipo` | select | 📅 Evento / 🚧 Proyecto / ⚡ Examen / 📝 Tarea |
| `Fecha Entrega` | date | Deadline de la tarea |
| `Días Restantes` | formula | Calculado automáticamente |
| `Área/Curso` | relation | Relación con BD_AREAS |
| `Aporte` | select | Aporte 1 / Aporte 2 / Aporte 3 |
| `Creado el` | created_time | Fecha de creación |
| `Última edición` | last_edited_time | Última modificación |

### Valores de Estado
```yaml
por_hacer:
  id: "cdf43d45-fd85-4710-99bb-671d8e989272"
  name: "Por hacer"
  color: "default"

en_progreso:
  id: "0d16944d-76fe-4a01-8cb4-96b363015b0a"
  name: "En progreso"
  color: "blue"

listo:
  id: "0a19a033-dcf4-45d9-8399-a0b6e142047c"
  name: "Listo"
  color: "green"
```

### Valores de Prioridad

> **Nota**: Los IDs de select options son generados por Notion en formato Base62 con caracteres especiales. Son válidos y funcionales tal cual. No editarlos manualmente.

```yaml
alta:
  id: "xkx?"
  name: "🔥 Alta"
  color: "red"

media:
  id: "r\\Ce"
  name: "⚡ Media"
  color: "default"

baja:
  id: "B~Y`"
  name: "☁️ Baja"
  color: "brown"
```

### Valores de Tipo
```yaml
evento:
  id: "HDHV"
  name: "📅 Evento"
  color: "gray"

proyecto:
  id: "uEF_"
  name: "🚧 Proyecto"
  color: "brown"

examen:
  id: "TGeV"
  name: "⚡ Examen"
  color: "default"

tarea:
  id: "qSkR"
  name: "📝 Tarea"
  color: "yellow"
```

---

## Ejemplos de Uso MCP

### Consultar Tareas Pendientes
```
Tool: mcp_notion-mcp-server_API-query-data-source
Params:
  data_source_id: "2cbaacd6-8210-803b-b9d9-d78fa3066b2a"
  filter:
    property: "Estado"
    status:
      does_not_equal: "Listo"
```

### Crear Nueva Tarea
```
Tool: mcp_notion-mcp-server_API-post-page
Params:
  parent:
    database_id: "2cbaacd6-8210-803b-b9d9-d78fa3066b2a"
  properties:
    Tarea:
      title:
        - text:
            content: "Nombre de la tarea"
    Estado:
      status:
        name: "Por hacer"
    Prioridad:
      select:
        name: "🔥 Alta"
    Tipo:
      select:
        name: "📝 Tarea"
    Fecha Entrega:
      date:
        start: "2026-02-10"
```

### Actualizar Estado de Tarea
```
Tool: mcp_notion-mcp-server_API-patch-page
Params:
  page_id: "<ID_DE_LA_TAREA>"
  properties:
    Estado:
      status:
        name: "En progreso"
```

---

## Cursos del Semestre 2026-1 (IDs)

```yaml
# Creados el 2026-02-04 en BD_AREAS - 6 cursos universitarios
CURSO_ECONOMIA_AMBIENTAL: "2fdaacd6-8210-81ae-bffe-f00d7ebaf358"
CURSO_ECONOMIA_INTERNACIONAL: "2fdaacd6-8210-8176-95da-f8f559269cc1"
CURSO_ECONOMIA_GESTION_PUBLICA: "2fdaacd6-8210-81a1-91d1-ce49066ad036"
CURSO_INVESTIGACION_OPERATIVA: "2fdaacd6-8210-8133-9234-c6de69555825"
CURSO_TEORIA_MONETARIA: "2fdaacd6-8210-8108-bb2a-ef7bba8a5825"
CURSO_INVESTIGACION_ECONOMICA: "2fdaacd6-8210-8143-8a86-f17fd377fe70"
```

---

## Cursos Personales (IDs)

```yaml
# Cursos independientes, no universitarios
CURSO_INGLES: "2fdaacd6-8210-8134-aa64-df39374251ed"  # Curso de inglés personal
```

---

## NotebookLM - Correlación con Cursos

```yaml
# IDs de Notebooks en librería local (notebook_manager.py)
# Fecha sincronización: 2026-02-04

NOTEBOOK_ECONOMIA_AMBIENTAL:
  id: "economia-ambiental"
  url: "https://notebooklm.google.com/notebook/3a62837e-ddff-4aac-b1ce-4847fd90e842"
  curso_id: "CURSO_ECONOMIA_AMBIENTAL"

NOTEBOOK_ECONOMIA_INTERNACIONAL:
  id: "economia-internacional-i"
  url: "https://notebooklm.google.com/notebook/2efe8c43-6888-446f-803d-5f57a9485ecb"
  curso_id: "CURSO_ECONOMIA_INTERNACIONAL"

NOTEBOOK_ECONOMIA_GESTION_PUBLICA:
  id: "economia-y-gestion-publica"
  url: "https://notebooklm.google.com/notebook/b62f9068-a5a0-4647-a9bb-2e7a15001d9d"
  curso_id: "CURSO_ECONOMIA_GESTION_PUBLICA"

NOTEBOOK_INVESTIGACION_OPERATIVA:
  id: "investigacion-operativa"
  url: "https://notebooklm.google.com/notebook/7dca47a9-fa22-438b-b05a-d4204ccf0242"
  curso_id: "CURSO_INVESTIGACION_OPERATIVA"

NOTEBOOK_TEORIA_MONETARIA:
  id: "teoria-monetaria-y-bancaria"
  url: "https://notebooklm.google.com/notebook/db8832ff-e387-4345-8d91-891984ba8636"
  curso_id: "CURSO_TEORIA_MONETARIA"

NOTEBOOK_INVESTIGACION_ECONOMICA:
  id: "investigacion-economica"
  url: "https://notebooklm.google.com/notebook/79852344-04fa-41ac-9988-b888d65f09a2"
  curso_id: "CURSO_INVESTIGACION_ECONOMICA"

NOTEBOOK_INGLES:
  id: "ingles"
  url: "https://notebooklm.google.com/notebook/c2607741-3ec8-4cd0-8fa5-5158712299b9"
  curso_id: "CURSO_INGLES"

NOTEBOOK_COGNITIVE_ALPHA:
  id: "cognitive-alpha"
  url: "https://notebooklm.google.com/notebook/a5c34c09-5b05-4ff0-9f7d-bff04972c546"
  descripcion: "Proyecto Active Recall - Optimización de aprendizaje"
```

### Tabla de Correlación Rápida

| Curso | Notebook ID | Comando Brain OS |
|-------|-------------|------------------|
| 📗 Economía Ambiental | `economia-ambiental` | "Consulta mi libro de Economía Ambiental" |
| 📘 Economía Internacional I | `economia-internacional-i` | "Consulta mi libro de Economía Internacional" |
| 📙 Economía y Gestión Pública | `economia-y-gestion-publica` | "Consulta mi libro de Gestión Pública" |
| 📕 Investigación Operativa | `investigacion-operativa` | "Consulta mi libro de Investigación Operativa" |
| 📔 Teoría Monetaria y Bancaria | `teoria-monetaria-y-bancaria` | "Consulta mi libro de Teoría Monetaria" |
| 📓 Investigación Económica | `investigacion-economica` | "Consulta mi libro de Investigación Económica" |
| 📒 Inglés | `ingles` | "Consulta mi libro de Inglés" |
| 🧠 Cognitive Alpha | `cognitive-alpha` | "Consulta Cognitive Alpha" |

### Uso Recomendado por Sesión
1. **Audio Overview**: Escuchar resumen 5 min antes de estudiar
2. **Q&A**: Hacer preguntas durante Pomodoro
3. **Info Report**: Generar síntesis post-estudio

### Flujo Híbrido B+C (Nuevo)

```yaml
# Archivos del Flujo:
template: templates/notebooklm_content_template.md
registry: config/notebooklm_registry.json
workflow: .agent/workflows/brain-os-study.md (sección NotebookLM)
skill: skills/notebooklm/SKILL.md
```

#### Comando: "Prepara contenido para NotebookLM de [curso]"
1. Brain OS lee índice/syllabus del curso
2. Usa template universal para generar documento
3. Usuario copia y pega en NotebookLM
4. Usuario activa "Investigar"

#### Comando: "Consulta mi libro de [curso]: [pregunta]"
1. Brain OS busca notebook en registry
2. Ejecuta skill notebooklm
3. Retorna respuesta grounded

#### Estado de Contenido por Curso
| Curso | NotebookLM | Contenido Generado |
|-------|------------|-------------------|
| 📗 Economía Ambiental | ✅ | Pendiente |
| 📘 Economía Internacional | ✅ | Pendiente |
| 📙 Economía y Gestión | ✅ | Pendiente |
| 📕 Investigación Operativa | ✅ | Pendiente |
| 📔 Teoría Monetaria | ✅ | Pendiente |
| 📓 Investigación Económica | ✅ | Pendiente |
| 📒 Inglés | ✅ | ✅ Activo (65 fuentes) |

---

## 🍅 Pomodoro Timer - Herramienta de Sesiones

```yaml
# Ubicación: tools/pomodoro/
# Archivo principal: pomodoro_timer.py
# Skill asociada: skills/pomodoro/SKILL.md

POMODORO_TOOL:
  location: "tools/pomodoro/"
  config_file: "config.json"
  state_file: "state.json"
  history_file: "history.json"
  
  profiles:
    default: {work: 25, break: 5}
    intensive: {work: 50, break: 10}
    light: {work: 15, break: 3}
    exam_prep: {work: 45, break: 8}
    ultradian: {work: 90, break: 20}  # BRAC fisiológico — Deep Research
  
  adaptive_rules:
    calculo|fisica|algebra: "intensive"
    ingles|lectura|repaso: "light"
    examen|parcial|final: "exam_prep"
    investigacion operativa|simplex|programacion lineal: "ultradian"
    economia internacional|comercio|aranceles: "ultradian"
    tesis|paper|ensayo largo|monografia: "ultradian"
  
  active_recall:
    enabled: true
    questions_per_session: 3
    bloom_levels: ["apply", "analyze", "evaluate"]

  notion_sync:
    database_id: "2cbaacd6-8210-8064-bd2e-c5eccf539edc"  # BD_TRACKER_DIARIO
    property: "🍅 Pomodoros"
    auto_sync: true
```

---

## 🧬 Cronobiología — Perfil del Usuario

```yaml
# Basado en Deep Research: Gestión de Energía vs Tiempo
# Fecha de configuración: 2026-02-12

CRONOTIPO: "Bear"  # Lion|Bear|Wolf|Dolphin

HORARIOS:
  despertar_clases_7am: "06:00"   # MA/JU
  despertar_clases_9_11am: "08:30" # L/MI/VI
  despertar_sin_clases: "09:00"   # S/D
  almuerzo: "~14:30"
  dormir: "23:30–00:00"
  dip_energetico: "~16:00"

PEAK_COGNITIVO_BEAR:
  peak: "10:00–14:00"      # Estudio profundo, BRAC 90/20
  dip: "14:00–16:00"       # Siesta NSDR 15min o tarea mecánica
  recovery: "16:00–18:00"  # Segunda ventana, menor intensidad
  wind_down: "18:00–23:00" # Revisión ligera

PROTOCOLOS_ENERGIA:
  luz_natural: "10 min post-despertar"
  cafe_retrasado: "90 min post-despertar (ideal)"
  siesta_nsdr: "10-20 min en dip (14:00-15:00)"
  pre_sueno: "Sin pantallas brillantes 22:00+"

ESTUDIO:
  preferencia: "sesiones largas y pocas"  # Alinea con ultradian
  meta_diaria: 1  # Mínimo 1 sesión/día, incluso S/D
  materias_dificiles: ["Economía Internacional", "Investigación Operativa"]
  materias_faciles: ["Teoría Monetaria y Bancaria", "Investigación Económica"]
```

### Comandos del Timer
| Comando | Descripción |
|---------|-------------|
| `start --topic "X"` | Inicia con modo auto-detectado |
| `status` | Estado actual (JSON) |
| `pause / resume` | Control de sesión |
| `stop` | Detiene y registra |
| `history --period week` | Analytics |

---

## Aula Virtual UAndina - Correlación de Cursos

```yaml
# Mapeo: Nombre Moodle → Brain OS ID → Notion ID
# Archivo fuente: skills/aula-virtual/scripts/course_map.py
# Última actualización: 2026-02-05

AULA_VIRTUAL_ECONOMIA_AMBIENTAL:
  moodle_patterns: ["ECONOMIA AMBIENTAL", "ECON AMBIENT"]
  brain_os_id: "economia_ambiental"
  notion_id: "2fdaacd6-8210-81ae-bffe-f00d7ebaf358"
  emoji: "📗"

AULA_VIRTUAL_ECONOMIA_INTERNACIONAL:
  moodle_patterns: ["ECONOMIA INTERNACIONAL", "ECON INTER"]
  brain_os_id: "economia_internacional"
  notion_id: "2fdaacd6-8210-8176-95da-f8f559269cc1"
  emoji: "📘"

AULA_VIRTUAL_GESTION_PUBLICA:
  moodle_patterns: ["GESTION PUBLICA", "GESTIÓN PÚBLICA"]
  brain_os_id: "economia_gestion_publica"
  notion_id: "2fdaacd6-8210-81a1-91d1-ce49066ad036"
  emoji: "📙"

AULA_VIRTUAL_INVESTIGACION_OPERATIVA:
  moodle_patterns: ["INVESTIGACION OPERATIVA", "INV OPER"]
  brain_os_id: "investigacion_operativa"
  notion_id: "2fdaacd6-8210-8133-9234-c6de69555825"
  emoji: "📕"

AULA_VIRTUAL_TEORIA_MONETARIA:
  moodle_patterns: ["TEORIA MONETARIA", "MONETARIA Y BANCARIA"]
  brain_os_id: "teoria_monetaria"
  notion_id: "2fdaacd6-8210-8108-bb2a-ef7bba8a5825"
  emoji: "📔"

AULA_VIRTUAL_INVESTIGACION_ECONOMICA:
  moodle_patterns: ["INVESTIGACION ECONOMICA", "INV ECON"]
  brain_os_id: "investigacion_economica"
  notion_id: "2fdaacd6-8210-8143-8a86-f17fd377fe70"
  emoji: "📓"

AULA_VIRTUAL_INGLES:
  moodle_patterns: ["INGLES", "INGLÉS", "ENGLISH"]
  brain_os_id: "ingles"
  notion_id: "2fdaacd6-8210-8134-aa64-df39374251ed"
  emoji: "📒"
  tipo: "personal"  # No es curso universitario
```

### Flujo de Sincronización
```
1. Moodle → download_files.py → Archivos Locales + .url
2. Archivos Locales → sync_full_local.py → Notion BD_RECURSOS (Links + Archivos)
3. Moodle → sync_assignments.py → Notion BD_TAREAS_MAESTRAS
```
