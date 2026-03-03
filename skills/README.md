# Skills Directory — Brain OS v2.1

> **42 skills especializadas** para potenciar el sistema Brain OS.

---

## 📂 Estructura

Cada skill vive en su propia carpeta:

```
skills/
├── skill-name/
│   ├── SKILL.md             # Definición principal (obligatorio)
│   ├── scripts/             # Scripts ejecutables (opcional)
│   ├── references/          # Documentación auxiliar (opcional)
│   └── assets/              # Templates y recursos (opcional)
└── _archive/                # Skills archivadas/reemplazadas
```

---

## Categorías de Skills

### 🎓 Académicas (Core Brain OS)

| Skill | Función |
|-------|---------|
| `aula-virtual` | Integración con Moodle UAndina — tareas, notas, materiales |
| `notebooklm` | Consultas a NotebookLM — grounded answers por curso |
| `pomodoro` | Timer Pomodoro adaptativo (5 modos + Active Recall) |
| `library-manager` | Ingesta de archivos + Progressive Summarization |

### ⚙️ Sistema (Core Brain OS)

| Skill | Función |
|-------|---------|
| `system-coordinator` | Auditoría técnica, verificación de integridad |
| `dashboard-sync` | Sincroniza INICIO.md con estado del sistema |
| `cleanup-manager` | Limpieza de archivos obsoletos — 4 niveles |
| `elite-skill-architect` | Meta-skill: crear, auditar, rehacer e implementar skills |
| `architecture` | ADRs, análisis de estructura, patrones de diseño |

### 📋 Planificación

| Skill | Función |
|-------|---------|
| `planning` | Planes accionables con pasos atómicos y verificación |
| `planning-with-files` | Planificación persistente estilo Manus (task_plan.md) |
| `executing-plans` | Ejecutar planes por batches con checkpoints |

### ✍️ Escritura y Documentación

| Skill | Función |
|-------|---------|
| `brainstorming` | Diseño validado antes de implementar — 7 pasos |
| `doc-coauthoring` | Co-autoría de documentos estructurados |
| `copywriting` | Copywriting de marketing enfocado en conversión |
| `copy-editing` | Edición de copy — 7 sweeps framework |
| `content-creator` | Contenido SEO + brand voice + redes sociales |
| `writing-skills` | Herramientas para escribir y validar skills |

### 🔍 Investigación y Análisis

| Skill | Función |
|-------|---------|
| `research-engineer` | Ingeniero de investigación — rigor científico |
| `prompt-engineer` | Diseño y optimización de prompts para LLMs |
| `prompt-engineering` | Técnicas avanzadas de prompt engineering |
| `prompt-library` | Biblioteca de prompts reutilizables |
| `last30days` | Investigación de actualidad en Reddit + X + Web (30 días) |

### 📄 Documentos y Formatos

| Skill | Función |
|-------|---------|
| `pdf` | Manipulación de PDFs (extraer, crear, merge, OCR) |
| `docx-official` | Creación y edición de documentos Word |
| `pptx-official` | Creación de presentaciones PowerPoint |
| `xlsx-official` | Trabajo con hojas de cálculo Excel |

### 🧩 Utilidades

| Skill | Función |
|-------|---------|
| `documentation-templates` | Templates de documentación |
| `notion-template-business` | Templates de Notion para negocios |
| `kaizen` | Mejora continua |

### ⚙️ Sistema Avanzado (Nuevo)

| Skill | Función |
|-------|---------|
| `agent-memory-systems` | Arquitectura de memoria del agente — episódica, semántica, procedimental |
| `context-window-management` | Estrategias de gestión de ventana de contexto y tokens |
| `autonomous-agent-patterns` | Patrones del agent loop (Think → Decide → Act → Observe) |
| `skill-orchestrator` | Índice maestro de 240+ skills — descubrimiento y combos |
| `conversation-memory` | Memoria persistente entre sesiones — Hemingway Bridge estructurado |

### 🛠️ Dev Tools (Nuevo)

| Skill | Función |
|-------|---------|
| `mcp-builder` | Guía para construir servidores MCP personalizados |
| `personal-tool-builder` | Patrón para crear herramientas CLI personales |
| `workflow-automation` | Diseño de flujos durables — secuencial, paralelo, orchestrator |

### 🧪 Calidad (Nuevo)

| Skill | Función |
|-------|---------|
| `systematic-debugging` | Debugging metódico — 5 pasos reproducibles |
| `playwright-skill` | Automatización de browser con Playwright |

### 🧠 Comportamiento (Nuevo)

| Skill | Función |
|-------|---------|
| `behavioral-modes` | Modos operativos adaptativos: TEACH, BRAINSTORM, DEBUG, REVIEW, IMPLEMENT |

### 🧹 Organización (Nuevo)

| Skill | Función |
|-------|---------|
| `file-organizer` | Audita y reorganiza `carrera/` — detecta duplicados y clasifica archivos |

### 📦 Archivadas (`_archive/`)

Skills reemplazadas por versiones fusionadas:
- `concise-planning` → fusionada en `planning`
- `plan-writing` → fusionada en `planning`
- `writing-plans` → fusionada en `planning`

---

## Cómo Usar

Las skills se activan automáticamente cuando el agente detecta un trigger en la conversación.

Ejemplos:
```
"Audita la skill pomodoro"          → activa elite-skill-architect
"Quiero estudiar Inv. Operativa"    → activa pomodoro
"Planifica cómo agregar X"          → activa planning
"Escanear basura"                   → activa cleanup-manager
```

---

## Crear Skills Nuevas

Usar la skill `elite-skill-architect`:
1. **Diseño**: "Quiero crear una skill" → entrevista → prompt maestro
2. **Implementación**: "Implementa la skill [nombre]" → directorio + archivos
3. **Auditoría**: "Audita la skill [nombre]" → score /100 + brechas
