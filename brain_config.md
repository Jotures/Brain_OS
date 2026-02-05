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
Moodle → get_tasks.py → course_map.py → sync_to_notion.py → BD_TAREAS_MAESTRAS
```
