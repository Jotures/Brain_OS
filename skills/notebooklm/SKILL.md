---
name: notebooklm
description: Consulta tus notebooks de Google NotebookLM directamente desde el agente para respuestas grounded con citaciones desde Gemini. Motor v2 HTTP directo (notebooklm-py) + fallback browser. Gestión de biblioteca, audio overviews, quizzes y auth persistente. Usar cuando el usuario mencione NotebookLM o quiera consultar sus documentos.
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers.

## ⚡ Motor v2 (PRIMARIO — notebooklm-py)

> **El motor v2 usa HTTP directo en lugar de browser automation. Es ~10× más rápido y más estable.**
> Si v2 falla (sesión expirada, API rota), escalar al motor v1 (Patchright) como fallback.

### Auth v2 (solo primera vez)

```bash
# Login con Google (una vez, abre browser visible)
.venv\Scripts\notebooklm login

# Verificar estado
python scripts/run.py notebooklm_client.py
```

---

### 💬 Query (Chat grounded)

```bash
python scripts/run.py ask_question_v2.py --question "¿Qué es la ventaja comparativa?" --notebook-id economia-internacional-i
python scripts/run.py ask_question_v2.py --question "..." --notebook-url "https://notebooklm.google.com/notebook/..."
python scripts/run.py ask_question_v2.py --question "..." --notebook-id economia-ambiental --json-output
```

---

### 🎙️ Resumen en Audio

```bash
python scripts/run.py download_audio.py --notebook-id economia-internacional-i --output audio.mp3
python scripts/run.py download_audio.py --notebook-id operativa --output audio.mp3 --instructions "Hazlo conciso y en español"
```

---

### 🎬 Resumen en Video

```bash
python scripts/run.py generate_video.py --notebook-id economia-ambiental --output video.mp4
python scripts/run.py generate_video.py --notebook-id investigacion-operativa --output io_video.mp4 --instructions "Enfócate en algoritmos"
```

---

### 📊 Presentación (Slide Deck)

```bash
python scripts/run.py generate_slide_deck.py --notebook-id economia-internacional-i --output presentacion.pptx
python scripts/run.py generate_slide_deck.py --notebook-id operativa --output io_slides.pptx --instructions "Incluye diagrams de flujo"
```

---

### 🗺️ Mapa Mental

```bash
python scripts/run.py generate_mind_map.py --notebook-id economia-ambiental --output mapa.json
python scripts/run.py generate_mind_map.py --notebook-id economia-ambiental --instructions "Foco en instrumentos económicos" --output mapa.json
```

---

### 📄 Informes (Reports)

```bash
# Tipos disponibles: briefing_doc | study_guide | blog_post | custom
python scripts/run.py generate_report.py --notebook-id economia-ambiental --type briefing_doc --output briefing.md
python scripts/run.py generate_report.py --notebook-id operativa --type study_guide --output guia.md
python scripts/run.py generate_report.py --notebook-id economia-ambiental --type blog_post --output blog.md
python scripts/run.py generate_report.py --notebook-id economia-ambiental --type custom --prompt "Haz un análisis de política pública" --output custom.md
```

---

### 📝 Cuestionario (Quiz)

```bash
# difficulty: easy|medium|hard | quantity: fewer|standard|more
python scripts/run.py generate_quiz.py --notebook-id economia-ambiental --format markdown
python scripts/run.py generate_quiz.py --notebook-id operativa --difficulty hard --quantity more --format json --output quiz.json
```

---

### 🗂️ Tarjetas Didácticas (Flashcards)

```bash
python scripts/run.py generate_flashcards.py --notebook-id economia-internacional-i --output flashcards.md
python scripts/run.py generate_flashcards.py --notebook-id operativa --difficulty hard --quantity more --output flashcards_io.md
```

---

### 🖼️ Infografía

```bash
# orientation: portrait|landscape|square
python scripts/run.py generate_infographic.py --notebook-id economia-ambiental --output infografia.png
python scripts/run.py generate_infographic.py --notebook-id operativa --orientation landscape --output io_infografia.png
```

---

### 📋 Tabla de Datos

```bash
python scripts/run.py generate_data_table.py --notebook-id economia-ambiental --output tabla.csv
python scripts/run.py generate_data_table.py --notebook-id operativa --instructions "Extrae complejidades de los algoritmos" --output tabla.json
```

---

### Resumen Rápido de Comandos v2

| Capacidad | Script | Salida |
|-----------|--------|--------|
| Query/Chat | `ask_question_v2.py` | texto |
| Audio Overview | `download_audio.py` | `.mp3` |
| Video Overview | `generate_video.py` | `.mp4` |
| Presentación | `generate_slide_deck.py` | `.pptx` |
| Mapa Mental | `generate_mind_map.py` | `.json` |
| Informe | `generate_report.py` | `.md/.html` |
| Quiz | `generate_quiz.py` | `.md/.json` |
| Flashcards | `generate_flashcards.py` | `.md/.json` |
| Infografía | `generate_infographic.py` | `.png` |
| Tabla de Datos | `generate_data_table.py` | `.csv/.json` |

---

### Flujo de Degradación v2 → v1

```
Nivel 0 — Motor v2 (HTTP directo)
  → python scripts/run.py ask_question_v2.py --question "..." --notebook-id ID
  → Si falla con "Sesión expirada": .venv\Scripts\notebooklm login → Reintentar
  → Si falla con otro error: ir a Nivel 1

Nivel 1 — Motor v1 (Patchright browser — fallback)
  → python scripts/run.py ask_question.py --question "..." --notebook-id ID
  → Si falla: seguir protocolo original de degradación (Nivel 2-4 abajo)
```

---

## 🔧 Motor v1 (FALLBACK — Patchright Browser)

> Motor original de browser automation. Mantenido como fallback.
> Solo usar si el motor v2 falla.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook"
- **NEW**: Says "Prepara contenido para NotebookLM de [curso]"
- **NEW**: Says "Consulta mi libro de [curso]"

## 📚 Flujo Híbrido B+C (Global)

### Preparar Contenido (Brain OS → Usuario → NotebookLM)
Cuando usuario dice: "Prepara contenido para NotebookLM de [curso]"
1. Leer índice/syllabus del curso
2. Usar template `templates/notebooklm_content_template.md`
3. Generar documento formateado
4. Usuario copia y pega en NotebookLM
5. Usuario activa "Investigar"

### Consultar Contenido (Brain OS ← NotebookLM)
Cuando usuario dice: "Consulta mi libro de [curso]: [pregunta]"
1. Buscar notebook en `config/notebooklm_registry.json`
2. Ejecutar query con `ask_question.py`
3. Retornar respuesta grounded

### Registro de Notebooks
```yaml
Archivo: config/notebooklm_registry.json
Formato: {"mapping": {"curso_id": "notebook_id"}}
```

## ⚠️ CRITICAL: Add Command - Smart Discovery

When user wants to add a notebook without providing details:

**SMART ADD (Recommended)**: Query the notebook first to discover its content:
```bash
# Step 1: Query the notebook about its content
python scripts/run.py ask_question.py --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" --notebook-url "[URL]"

# Step 2: Use the discovered information to add it
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[Based on content]" --description "[Based on content]" --topics "[Based on content]"
```

**MANUAL ADD**: If user provides all details:
- `--url` - The NotebookLM URL
- `--name` - A descriptive name
- `--description` - What the notebook contains (REQUIRED!)
- `--topics` - Comma-separated topics (REQUIRED!)

NEVER guess or use generic descriptions! If details missing, use Smart Add to discover them.

## Critical: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# ✅ CORRECT - Always use run.py:
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# ❌ WRONG - Never call directly:
python scripts/auth_manager.py status  # Fails without venv!
```

The `run.py` wrapper automatically:
1. Creates `.venv` if needed
2. Installs all dependencies
3. Activates environment
4. Executes script properly

## Core Workflow

### Step 1: Check Authentication Status
```bash
python scripts/run.py auth_manager.py status
```

If not authenticated, proceed to setup.

### Step 2: Authenticate (One-Time Setup)
```bash
# Browser MUST be visible for manual Google login
python scripts/run.py auth_manager.py setup
```

**Important:**
- Browser is VISIBLE for authentication
- Browser window opens automatically
- User must manually log in to Google
- Tell user: "A browser window will open for Google login"

### Step 3: Manage Notebook Library

```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# BEFORE ADDING: Ask user for metadata if unknown!
# "What does this notebook contain?"
# "What topics should I tag it with?"

# Add notebook to library (ALL parameters are REQUIRED!)
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Descriptive Name" \
  --description "What this notebook contains" \  # REQUIRED - ASK USER IF UNKNOWN!
  --topics "topic1,topic2,topic3"  # REQUIRED - ASK USER IF UNKNOWN!

# Search notebooks by topic
python scripts/run.py notebook_manager.py search --query "keyword"

# Set active notebook
python scripts/run.py notebook_manager.py activate --id notebook-id

# Remove notebook
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### Quick Workflow
1. Check library: `python scripts/run.py notebook_manager.py list`
2. Ask question: `python scripts/run.py ask_question.py --question "..." --notebook-id ID`

### Step 4: Ask Questions

```bash
# Basic query (uses active notebook if set)
python scripts/run.py ask_question.py --question "Your question here"

# Query specific notebook
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Query with notebook URL directly
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Show browser for debugging
python scripts/run.py ask_question.py --question "..." --show-browser
```

## Follow-Up Mechanism (CRITICAL)

Every NotebookLM answer ends with: **"EXTREMELY IMPORTANT: Is that ALL you need to know?"**

**Required Claude Behavior:**
1. **STOP** - Do not immediately respond to user
2. **ANALYZE** - Compare answer to user's original request
3. **IDENTIFY GAPS** - Determine if more information needed
4. **ASK FOLLOW-UP** - If gaps exist, immediately ask:
   ```bash
   python scripts/run.py ask_question.py --question "Follow-up with context..."
   ```
5. **REPEAT** - Continue until information is complete
6. **SYNTHESIZE** - Combine all answers before responding to user

## Script Reference

### Authentication Management (`auth_manager.py`)
```bash
python scripts/run.py auth_manager.py setup    # Initial setup (browser visible)
python scripts/run.py auth_manager.py status   # Check authentication
python scripts/run.py auth_manager.py reauth   # Re-authenticate (browser visible)
python scripts/run.py auth_manager.py clear    # Clear authentication
```

### Notebook Management (`notebook_manager.py`)
```bash
python scripts/run.py notebook_manager.py add --url URL --name NAME --description DESC --topics TOPICS
python scripts/run.py notebook_manager.py list
python scripts/run.py notebook_manager.py search --query QUERY
python scripts/run.py notebook_manager.py activate --id ID
python scripts/run.py notebook_manager.py remove --id ID
python scripts/run.py notebook_manager.py stats
```

### Question Interface (`ask_question.py`)
```bash
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL] [--show-browser]
```

### Data Cleanup (`cleanup_manager.py`)
```bash
python scripts/run.py cleanup_manager.py                    # Preview cleanup
python scripts/run.py cleanup_manager.py --confirm          # Execute cleanup
python scripts/run.py cleanup_manager.py --preserve-library # Keep notebooks
```

### Book Analysis (`analyze_book.py`)
```bash
python scripts/run.py analyze_book.py --notebook-id ID --chapters "1, 8"
```

### Save Output to File (`query_to_file.py`)
```bash
# Safely save query output to file (avoids encoding issues)
python scripts/run.py query_to_file.py --notebook-id ID --question "..." --output filename.txt
```

## Environment Management

The virtual environment is automatically managed:
- First run creates `.venv` automatically
- Dependencies install automatically
- Chromium browser installs automatically
- Everything isolated in skill directory

Manual setup (only if automatic fails):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python -m patchright install chromium
```

## Data Storage

All data stored in `~/.claude/skills/notebooklm/data/`:
- `library.json` - Notebook metadata
- `auth_info.json` - Authentication status
- `browser_state/` - Browser cookies and session

**Security:** Protected by `.gitignore`, never commit to git.

## Configuration

Optional `.env` file in skill directory:
```env
HEADLESS=false           # Browser visibility
SHOW_BROWSER=false       # Default browser display
STEALTH_ENABLED=true     # Human-like behavior
TYPING_WPM_MIN=160       # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=     # Default notebook
```

## Decision Flow

```
User mentions NotebookLM
    ↓
Check auth → python scripts/run.py auth_manager.py status
    ↓
If not authenticated → python scripts/run.py auth_manager.py setup
    ↓
Check/Add notebook → python scripts/run.py notebook_manager.py list/add (with --description)
    ↓
Activate notebook → python scripts/run.py notebook_manager.py activate --id ID
    ↓
Ask question → python scripts/run.py ask_question.py --question "..."
    ↓
See "Is that ALL you need?" → Ask follow-ups until complete
    ↓
Synthesize and respond to user
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper |
| Authentication fails | Browser must be visible for setup! --show-browser |
| Rate limit (50/day) | Wait or switch Google account |
| Browser crashes | `python scripts/run.py cleanup_manager.py --preserve-library` |
| Notebook not found | Check with `notebook_manager.py list` |

## Best Practices

1. **Always use run.py** - Handles environment automatically
2. **Check auth first** - Before any operations
3. **Follow-up questions** - Don't stop at first answer
4. **Browser visible for auth** - Required for manual login
5. **Include context** - Each question is independent
6. **Synthesize answers** - Combine multiple responses

## Limitations

- No session persistence (each question = new browser)
- Rate limits on free Google accounts (50 queries/day)
- Manual upload required (user must add docs to NotebookLM)
- Browser overhead (few seconds per question)

## 🛡️ Fallback: Degradación Graceful

Cuando el MCP de NotebookLM falle (Patchright roto, UI de Google cambió, rate limit, etc.):

### Protocolo de Degradación

```
Nivel 1 — Reintento
  → Ejecutar: python scripts/run.py ask_question.py --show-browser --question "test"
  → Si falla con error de browser: ir a Nivel 2

Nivel 2 — Reauth
  → Ejecutar: python scripts/run.py auth_manager.py reauth
  → Si falla: ir a Nivel 3

Nivel 3 — Fallback Local (sin dependencia externa)
  → Abrir PDF/libro desde carrera/semestres/2026-1/cursos/[curso]/01_Materiales/
  → Usar Ctrl+F para buscar el tema
  → Buscar en archivos locales con grep/ripgrep
  → Informar al usuario: "⚠️ NotebookLM no disponible. Consultando material local."

Nivel 4 — Reinstalar
  → python scripts/run.py cleanup_manager.py --confirm
  → python -m patchright install chromium
  → python scripts/run.py auth_manager.py setup
```

### Health Check Rápido

```bash
# Verificar que el MCP responde (ejecutar durante boot "Buenos días")
python scripts/run.py auth_manager.py status
```

| Estado | Significado | Acción |
|:------:|-------------|--------|
| ✅ Authenticated | Todo OK | Ninguna |
| ⚠️ Expired | Sesión expiró | `reauth` automático |
| ❌ Not authenticated | Sin auth | Setup manual (browser visible) |
| 💥 Script error | Patchright/Chromium roto | Nivel 4 (reinstalar) |

### Sobre la API Oficial de Google

> **Estado (Feb 2026)**: Google no ha publicado API oficial para NotebookLM.
> Si se publica, migrar de browser automation a API directa eliminaría la fragilidad.
> Monitorear: https://ai.google.dev/ y el changelog de NotebookLM.

## Resources (Skill Structure)

**Important directories and files:**

- `scripts/` - All automation scripts (ask_question.py, notebook_manager.py, etc.)
- `data/` - Local storage for authentication and notebook library
- `references/` - Extended documentation:
  - `api_reference.md` - Detailed API documentation for all scripts
  - `troubleshooting.md` - Common issues and solutions
  - `usage_patterns.md` - Best practices and workflow examples
- `.venv/` - Isolated Python environment (auto-created on first run)
- `.gitignore` - Protects sensitive data from being committed
