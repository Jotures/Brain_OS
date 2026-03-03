# 🧠 Guía Maestra de Skills — Brain OS v2.1

> **42 skills instaladas** | Actualizado: 2026-03-03

Esta guía te enseña a sacarle el máximo provecho a cada skill de Brain OS. Está organizada por **lo que quieres hacer**, no por categoría técnica.

---

## 📖 Cómo funcionan las Skills

Las skills son instrucciones especializadas que el agente lee automáticamente cuando detecta ciertos triggers en tu conversación. No necesitas activarlas manualmente — simplemente habla con naturalidad.

```
TÚ:     "Quiero estudiar Economía Internacional"
AGENTE: [lee skills/pomodoro/SKILL.md automáticamente]
        [configura el timer con el perfil correcto]
        [inicia la sesión]
```

Cada skill carpeta tiene:
- **`SKILL.md`** → Las instrucciones del agente (obligatorio)
- **`BRAIN_OS_CONTEXT.md`** → Cómo aplicar la skill en TU sistema Brain OS (adaptación personalizada)
- **`scripts/`** → Scripts ejecutables si los necesita
- **`references/`** → Documentación auxiliar

---

## 🎯 Índice Rápido por Tarea

| Quiero... | Skill(s) a usar |
|-----------|----------------|
| Estudiar con timer | `pomodoro` |
| Entender un concepto difícil | `behavioral-modes` (TEACH) + `notebooklm` |
| Hacer una tarea/trabajo | `planning` → `research-engineer` → `doc-coauthoring` → `docx-official` |
| Crear una presentación | `brainstorming` → `pptx-official` |
| Investigar un tema actual | `last30days` → `research-engineer` |
| Sincronizar con Moodle | `aula-virtual` |
| Organizar mis archivos | `file-organizer` → `library-manager` |
| Arreglar algo roto | `systematic-debugging` |
| Crear una skill nueva | `elite-skill-architect` |
| Saber qué skill usar | `skill-orchestrator` |

---

## 🎓 SKILLS ACADÉMICAS

> El corazón de Brain OS. Las usarás todos los días.

---

### 🍅 `pomodoro` — Timer Adaptativo de Estudio

**¿Cuándo usarla?** Siempre que quieras estudiar con enfoque.

**Triggers automáticos:**
- `"Quiero estudiar [materia]"`
- `"Inicia un Pomodoro"`
- `"Modo estudio"`

**5 Perfiles de Pomodoro disponibles:**
| Perfil | Foco | Descanso | Para qué |
|--------|------|----------|----------|
| `standard` | 25 min | 5 min | Tareas rutinarias |
| `deep-work` | 50 min | 10 min | Conceptos difíciles, matemáticas |
| `sprint` | 15 min | 3 min | Repasos rápidos, pre-examen |
| `creative` | 45 min | 15 min | Ensayos, trabajos creativos |
| `adaptive` | Variable | Variable | El agente decide según la materia |

**Al finalizar:** El agente activa modo TEACH → te hace 3 preguntas de Active Recall sobre lo estudiado. Esto mejora la retención a largo plazo.

---

### 🌐 `aula-virtual` — Integración con Moodle UAndina

**¿Cuándo usarla?** Para sincronizar tareas, notas y materiales de tus cursos.

**Triggers automáticos:**
- `"Sincroniza con Aula Virtual"`
- `"¿Qué tareas tengo pendientes?"`
- `"Descarga los materiales de [materia]"`

**Qué hace:**
- Descarga archivos nuevos de Moodle → los guarda en `carrera/semestres/2026-1/cursos/[MATERIA]/01_Materiales/`
- Sincroniza tareas y fechas de entrega con Notion (BD_TAREAS_MAESTRAS)
- Consulta calificaciones

**⚠️ Requiere:** Conexión a internet + credenciales de UAndina en variables de entorno.

---

### 📚 `notebooklm` — Consultas con Fuentes de Tus Cursos

**¿Cuándo usarla?** Cuando quieras respuestas basadas en tus materiales académicos, no en internet genérico.

**Triggers automáticos:**
- `"Pregúntale a NotebookLM sobre [tema]"`
- `"¿Qué dice el material de [materia] sobre [X]?"`
- `"Consulta grounded sobre [concepto]"`

**8 Notebooks disponibles** (uno por materia). NotebookLM responde **solo** con base en tus documentos → cero alucinaciones.

**Flujo recomendado:**
```
1. Subir materiales del curso → notebooklm
2. Consultar conceptos      → notebooklm (respuesta grounded)
3. Profundizar si es vago   → research-engineer
```

---

### 📥 `library-manager` — Gestor de Materiales Académicos

**¿Cuándo usarla?** Para ingresar nuevos archivos al sistema con Progressive Summarization.

**Triggers automáticos:**
- `"Guarda este archivo"`
- `"Ingesta este PDF"`
- `"Resume progresivamente [material]"`

**Las 4 capas de Progressive Summarization:**
1. **Captura** → Guardar el archivo en la carpeta correcta
2. **Negrita** → Marcar los conceptos más importantes
3. **Resaltado** → Seleccionar lo esencial de lo importante
4. **Resumen** → El agente genera síntesis ejecutiva

> 💡 No necesitas hacer las 4 capas de una vez. Puedes avanzar una capa cada sesión.

---

## ⚙️ SKILLS DE SISTEMA

> Las que mantienen Brain OS funcionando.

---

### 🔧 `system-coordinator` — Verificación de Integridad

**¿Cuándo usarla?** Para hacer un health check del sistema o cuando algo no funcione.

**Triggers automáticos:**
- `"Verifica el sistema"`
- `"¿Todo está bien?"`
- `"Health check"`

**Qué verifica:**
- IDs de Notion accesibles
- Notebooks de NotebookLM respondiendo
- Estructura de carpetas intacta

---

### 📊 `dashboard-sync` — Actualización del Dashboard INICIO.md

**¿Cuándo usarla?** Se activa automáticamente durante el boot diario (Paso 3).

**Triggers automáticos:**
- `"Actualiza el dashboard"`
- `"Regenera INICIO.md"`
- Parte del flujo `/buenos-dias`

**Qué genera:** Un archivo `INICIO.md` actualizado con el estado del día, tareas prioritarias, y el Hemingway Bridge del día anterior.

---

### 🧹 `cleanup-manager` — Limpieza de Archivos Obsoletos

**¿Cuándo usarla?** Cuando el sistema acumula archivos temporales o redundantes.

**Triggers automáticos:**
- `"Limpia el sistema"`
- `"Escanea basura"`
- `"Archivo obsoletos"`

**4 niveles de limpieza:**
| Nivel | Qué hace | Riesgo |
|-------|----------|--------|
| 1 | Eliminar archivos `.tmp`, logs vacíos | Ninguno |
| 2 | Archivar materiales de semestres pasados | Bajo |
| 3 | Deduplicar archivos idénticos | Medio |
| 4 | Reorganización profunda + confirmación | Requiere revisión |

---

### 🔍 `file-organizer` — Auditoría y Organización de `carrera/`

**¿Cuándo usarla?** Cuando tienes archivos sin clasificar o quieres auditar el orden de `carrera/`.

**Triggers:**
- `"Organiza mis archivos de [materia]"`
- `"Detecta duplicados en carrera/"`
- `"Audita la carpeta de [semestre]"`

**Estructura estándar que mantiene:**
```
carrera/semestres/2026-1/cursos/[MATERIA]/
├── 01_Materiales/   # PDFs, diapositivas
├── 02_Tareas/       # Trabajos entregados
├── 03_Apuntes/      # Notas personales
├── 04_Examenes/     # Material de evaluaciones
└── 05_Proyectos/    # Trabajos largos
```

> ⚠️ **Siempre pide confirmación antes de mover o eliminar.** Nunca actúa en silencio.

---

### 🏛️ `elite-skill-architect` — Crear y Auditar Skills

**¿Cuándo usarla?** Para construir nuevas skills o mejorar las existentes.

**Triggers:**
- `"Quiero crear una skill para [X]"`
- `"Audita la skill [nombre]"`
- `"Mejora la skill [nombre]"`

**3 modos de uso:**
1. **Diseño**: Entrevista → define el prompt maestro de la skill
2. **Implementación**: Crea el directorio + archivos de la skill
3. **Auditoría**: Score /100 con análisis de brechas y mejoras

---

## 📋 SKILLS DE PLANIFICACIÓN

---

### 🗺️ `planning` — Planes Accionables

**¿Cuándo usarla?** Para cualquier tarea compleja que requiera pasos ordenados.

**Triggers:**
- `"Planifica cómo [X]"`
- `"¿Cómo debería abordar [tarea]?"`
- `"Crea un plan para [X]"`

**Genera:** Un plan con pasos atómicos (cada paso = 1 acción concreta), criterios de verificación, y puntos de control.

---

### 📁 `planning-with-files` — Planificación Persistente

**¿Cuándo usarla?** Para planes de varios días que necesitas retomar.

**Triggers:**
- `"Plan persistente para [proyecto]"`
- `"Crea un task_plan.md para [X]"`

**Diferencia con `planning`:** Guarda el plan en un archivo `task_plan.md` que puedes actualizar entre sesiones. Estilo Manus.

---

### ⚡ `executing-plans` — Ejecutar Planes por Batches

**¿Cuándo usarla?** Cuando ya tienes un plan y quieres ejecutarlo sistemáticamente.

**Triggers:**
- `"Ejecuta el plan de [X]"`
- `"Comenzamos con el batch 1"`

**Método:** Divide el plan en batches de 3-5 tareas, ejecuta cada batch, verifica antes de continuar.

---

## 🔍 SKILLS DE INVESTIGACIÓN

---

### 🔬 `research-engineer` — Investigación con Rigor Académico

**¿Cuándo usarla?** Para investigar temas con profundidad y precisión académica.

**Triggers:**
- `"Investiga [tema]"`
- `"Deep research sobre [X]"`
- `"Análisis académico de [concepto]"`

**Características:**
- Cero alucinaciones: si no sabe, lo dice
- Critica tu premisa si está equivocada (es su protocolo)
- Aplica el método científico: hipótesis → revisión → implementación → verificación

> ⚠️ **Nota:** Esta skill es más técnica/científica que humanística. Para Economía, complementar con `last30days` para contexto actual.

---

### 📡 `last30days` — Investigación de Actualidad

**¿Cuándo usarla?** Para trabajos que necesitan contexto de lo que está pasando **ahora** (últimas 4 semanas).

**Triggers:**
- `"Investiga en Reddit/X sobre [tema] de los últimos 30 días"`
- `"last30days: [tema]"`
- `"¿Qué se dice actualmente sobre [X]?"`

**Casos de uso por materia:**
| Materia | Ejemplo |
|---------|---------|
| Economía Internacional | `"last30days: aranceles Trump 2026"` |
| Economía Ambiental | `"last30days: COP política climática Perú"` |
| Macroeconomía | `"last30days: BCRP inflación Peru"` |

**Funciona sin API keys** → usa WebSearch como fallback automático.

**Flujo recomendado:**
```
last30days → [panorama actual]
    ↓
research-engineer → [rigor académico]
    ↓
doc-coauthoring + docx-official → [entrega final]
```

---

### 🎯 `prompt-library` — Guardar Prompts que Funcionan

**¿Cuándo usarla?** Para guardar los mejores prompts de investigación y reutilizarlos.

**Triggers:**
- `"Guarda este prompt en la biblioteca"`
- `"Muéstrame los prompts de [materia]"`

---

## 📄 SKILLS DE DOCUMENTOS

---

### 📝 `docx-official` — Documentos Word Profesionales

**¿Cuándo usarla?** Para crear o editar archivos `.docx`.

**Triggers:**
- `"Crea un documento Word sobre [X]"`
- `"Edita este .docx"`
- `"Genera el informe en Word"`

**3 workflows:**
1. **Crear desde cero**: usa `docx-js` (JavaScript)
2. **Editar existente**: usa la librería OOXML (Python)
3. **Redlining (revisión)**: tracked changes para documentos de terceros

---

### 🎨 `pptx-official` — Presentaciones PowerPoint

**¿Cuándo usarla?** Para crear presentaciones académicas o de exposición.

**Triggers:**
- `"Crea una presentación sobre [X]"`
- `"Genera el PPTX de [tema]"`

**Paletas de color disponibles**: 18 opciones predefinidas (o el agente elige según el tema).

**Workflow:**
```
1. html2pptx: diseño HTML → PPTX con precisión
2. Validación visual: genera thumbnails para verificar layout
3. Ajuste fino si hay problemas de texto/posición
```

---

### 📊 `xlsx-official` — Hojas de Cálculo Excel

**¿Cuándo usarla?** Para trabajos con datos, modelos financieros, o análisis estadísticos.

**Triggers:**
- `"Crea una hoja de cálculo para [X]"`
- `"Analiza estos datos en Excel"`

**Estándar de fórmulas**: siempre usa fórmulas reales (`=SUM()`, `=AVERAGE()`), nunca valores calculados en Python y pegados como estáticos.

**Color coding estándar (modelos financieros):**
- 🔵 Azul = inputs del usuario
- ⚫ Negro = fórmulas calculadas
- 🟢 Verde = links de otras hojas
- 🔴 Rojo = links de otros archivos

---

### 📋 `pdf` — Manipulación de PDFs

**¿Cuándo usarla?** Para trabajar con archivos PDF.

**Triggers:**
- `"Combina estos PDFs"`
- `"Extrae el texto de [archivo.pdf]"`
- `"OCR este PDF escaneado"`

**Capacidades:**
| Acción | Herramienta |
|--------|-------------|
| Extraer texto | `pdfplumber` |
| Extraer tablas | `pdfplumber` |
| Crear PDFs | `reportlab` |
| Merge/split | `pypdf` o `qpdf` |
| OCR (escaneados) | `pytesseract` |
| Password protect | `pypdf` |

---

## ✍️ SKILLS DE ESCRITURA

---

### 🤝 `doc-coauthoring` — Co-autoría de Documentos

**¿Cuándo usarla?** Para redactar documentos largos y estructurados (ensayos, informes, propuestas).

**Triggers:**
- `"Escribamos [tipo de documento]"`
- `"Ayúdame a redactar [X]"`
- `"Co-autoría de [documento]"`

**3 etapas del workflow:**
1. **Context Gathering**: el agente recoge todo el contexto antes de escribir
2. **Refinement & Structure**: construye sección por sección con brainstorming iterativo
3. **Reader Testing**: prueba el documento con un agente "fresco" para detectar puntos ciegos

**Ideal para**: ensayos académicos, informes de investigación, trabajos de fin de semestre.

---

### 🧠 `brainstorming` — Diseño Validado Antes de Implementar

**¿Cuándo usarla?** Cuando necesitas explorar opciones antes de comprometerte con un enfoque.

**Triggers:**
- `"Lluvia de ideas para [X]"`
- `"¿Qué opciones tengo para [problema]?"`
- `"Brainstorming de [tema]"`

**El proceso de 7 pasos**: No es solo "dame ideas". Incluye validación de restricciones, análisis de pros/contras, y síntesis hacia una decisión.

---

## 🧠 SKILLS DE COMPORTAMIENTO

---

### 🔄 `behavioral-modes` — Modos Operativos Adaptativos

**¿Cuándo usarla?** Se activa **automáticamente** según el tipo de tarea. También puedes solicitarla explícitamente.

**Los 6 modos:**

| Modo | Trigger | Comportamiento |
|------|---------|----------------|
| 📚 **TEACH** | "Explícame [X]", "No entiendo [Y]" | Analogías, ejemplos del curso, progresión simple→complejo |
| 🧠 **BRAINSTORM** | "¿Qué opciones tengo?", "Diseñemos" | 3+ alternativas, diagramas, sin implementar todavía |
| 🔍 **DEBUG** | "No funciona", "¿Por qué falla?" | Síntoma → Causa → Solución → Prevención |
| 📋 **REVIEW** | "Revisa mi ensayo", "Feedback sobre [X]" | Categorizado: Crítico / Mejora / Bien |
| ⚡ **IMPLEMENT** | "Ejecuta", "Hazlo", "Inicia el boot" | Directo, sin texto de relleno, mínimas preguntas |
| 🔭 **EXPLORE** | "¿Qué debería estudiar?", Boot diario | Diagnóstico → Mapa de prioridades |

**Modo TEACH + Pomodoro**: Al terminar una sesión Pomodoro, el agente entra en TEACH automáticamente para el Active Recall.

---

## ⚙️ SKILLS DE SISTEMA AVANZADO

> Estas skills diseñan **cómo funciona el agente**, no qué hace. Las usas principalmente cuando quieras mejorar o extender Brain OS.

---

### 🗂️ `agent-memory-systems` — Arquitectura de Memoria

**¿Para qué?** Diseña cómo el agente recuerda información entre sesiones.

**Los 4 tipos de memoria de Brain OS:**
| Tipo | Dónde vive | Ejemplo |
|------|-----------|---------|
| Episódica | `sesiones/` | Log de lo que estudiaste hoy |
| Semántica | `brain_config.md` | IDs de Notion, mapping de cursos |
| Procedimental | `skills/` | Cómo hacer el boot, cómo iniciar Pomodoro |
| De trabajo | Contexto activo | Lo que estás haciendo ahora mismo |

---

### 🧵 `conversation-memory` — Hemingway Bridge Estructurado

**¿Cuándo usarla?** Para formalizar el hilo de memoria entre sesiones de estudio.

**El Hemingway Bridge** — formato estándar al cerrar cada sesión:

```markdown
## 🧵 Hemingway Bridge — [Fecha] | [Materia]

Estado al cierre: [qué se logró en 1-2 líneas]
Próximo paso exacto: [acción específica para retomar]
Contexto crítico: [qué no olvidar]
Pendientes: [ ] tarea 1  [ ] tarea 2
```

**Cuándo se lee:** En el Paso 5 del boot diario. El agente lo usa para darte el "próximo paso exacto" al inicio del día.

---

### 📦 `context-window-management` — Gestión de Contexto

**¿Para qué?** Optimiza cuánta información se carga en cada conversación para evitar que el agente "olvide" cosas importantes.

**Regla de prioridad de carga:**
- **Tier 1 (siempre)**: IDs de Notion, estado del día, tareas urgentes
- **Tier 2 (bajo demanda)**: Materiales de cursos, historial de sesiones
- **Tier 3 (nunca completo)**: Todos los logs históricos, todas las skills a la vez

---

### 🎯 `skill-orchestrator` — Directorio de 240+ Skills

**¿Cuándo usarla?** Cuando no sabes qué skill usar para una tarea específica.

**Trigger:**
- `"¿Qué skill uso para [X]?"`
- `"Muéstrame el catálogo de skills"`

Contiene el índice completo de la biblioteca `antigravity-awesome-skills`. Si una tarea requiere una habilidad que Brain OS no tiene instalada, `skill-orchestrator` te dice cuál install siguiente.

---

### 🤖 `autonomous-agent-patterns` — El Agent Loop de Brain OS

**¿Para qué?** Define el ciclo operativo del agente.

**El loop en acción durante el boot:**
```
Think  → Leer brain_config + INICIO.md + último Hemingway Bridge
Decide → Priorizar: ¿qué materia? ¿qué tarea? ¿qué modo?
Act    → Ejecutar: Pomodoro, sync Aula Virtual, guardar archivo
Observe→ Actualizar INICIO.md + escribir nuevo Hemingway Bridge
```

---

## 🛠️ SKILLS DE DEV TOOLS

> Para cuando quieras extender o construir sobre Brain OS.

---

### 🔌 `mcp-builder` — Construir Servidores MCP

**¿Cuándo usarla?** Para crear integraciones personalizadas que conecten Brain OS con servicios externos.

**MCPs candidatos para Brain OS:**
- `brain-os-mcp`: Wrapper ligero para operaciones frecuentes (tareas, Pomodoro, diagnóstico)
- `moodle-mcp`: API directa de Aula Virtual (alternativa más estable que Playwright)

---

### 🛠️ `personal-tool-builder` — Crear Herramientas CLI

**¿Cuándo usarla?** Para construir nuevas herramientas de línea de comandos al estilo del Pomodoro Timer.

**Estándar de tools en Brain OS:**
```
tools/[nombre]/
├── [nombre].py     # CLI con Click
├── config.json     # Configuración
├── state.json      # Estado actual
└── history.json    # Logs históricos
```

---

### ⚡ `workflow-automation` — Diseño de Flujos Durables

**¿Cuándo usarla?** Para diseñar flujos que deban ser robustos ante fallos.

**Los 3 flujos críticos de Brain OS:**
1. **Boot diario** — secuencial con tolerancia a fallos por paso
2. **Sync Aula Virtual → Notion** — orchestrator-worker con idempotencia
3. **Progressive Summarization** — secuencial con checkpoints por capa

---

## 🧪 SKILLS DE CALIDAD

---

### 🔍 `systematic-debugging` — Debugging Metódico

**¿Cuándo usarla?** Cuando un script o flujo del sistema falla.

**Los 5 pasos:**
1. **Identificar** → ¿Qué comando falló? ¿Mensaje de error?
2. **Verificar integridad** → Ejecutar `system-coordinator`
3. **Revisar logs** → `_cleanup_test_output.txt`, `tools/pomodoro/history.json`
4. **Reproducir en aislamiento** → Ejecutar solo el componente que falla
5. **Fix y verificar** → Aplicar mínimo fix + re-verificar sistema completo

**Problemas frecuentes y soluciones:**
| Problema | Solución rápida |
|----------|----------------|
| "ID no encontrado" en Notion | Actualizar `brain_config.md` |
| Timeout en Aula Virtual | Verificar MOODLE_TOKEN + reintentar |
| Playwright falla selector | Inspeccionar elemento + actualizar selector |

---

### 🎭 `playwright-skill` — Automatización de Browser

**¿Cuándo usarla?** Se activa internamente con `aula-virtual` y `notebooklm`. Raramente necesitas llamarla directo.

**Uso directo:**
- Cuando un selector de Moodle o NotebookLM falla y necesitas actualizarlo
- Para agregar nueva automatización web

---

## 🧩 SKILLS DE UTILIDADES

---

### 🔄 `kaizen` — Mejora Continua del Sistema

**¿Cuándo usarla?** Para auditorías semanales o cuando sientes que Brain OS podría funcionar mejor.

**Triggers:**
- `"Auditoría kaizen del sistema"`
- `"¿Qué podría mejorar en mi flujo de estudio?"`

---

### 📄 `documentation-templates` — Templates de Documentación

**¿Cuándo usarla?** Para crear documentación estructurada con formatos estandarizados.

---

## 🎯 COMBOS RECOMENDADOS

> Recetas de skills para las tareas más comunes.

---

### 📚 Sesión de Estudio Diaria
```
/buenos-dias          → Inicia el boot (system-coordinator + dashboard-sync)
    ↓
pomodoro              → Timer adaptativo según materia del día
    ↓
behavioral-modes TEACH→ Active Recall al terminar la sesión
    ↓
conversation-memory   → Escribe el Hemingway Bridge al cerrar
```

### 📝 Hacer una Tarea Académica
```
last30days            → Contexto de actualidad (si el tema es reciente)
    ↓
research-engineer     → Investigación con rigor académico
    ↓
brainstorming         → Estructura del trabajo
    ↓
doc-coauthoring       → Redacción colaborativa sección por sección
    ↓
docx-official / pdf   → Entrega final en el formato requerido
```

### 🎤 Preparar una Exposición
```
brainstorming         → Estructura narrativa de la presentación
    ↓
research-engineer     → Datos y evidencia de soporte
    ↓
pptx-official         → Presentación visual profesional
    ↓
behavioral-modes TEACH→ Modo TEACH para practicar la explicación
```

### 🆘 Modo Crisis (Pre-Examen)
```
behavioral-modes EXPLORE → Diagnóstico: ¿qué temas son más críticos?
    ↓
notebooklm               → Consultas rápidas a tus materiales
    ↓
pomodoro [sprint]        → Sesiones cortas de 15 min de repaso
    ↓
behavioral-modes TEACH   → Active Recall agresivo hasta el examen
```

### 🔧 Cuando Algo Falla en el Sistema
```
systematic-debugging     → Diagnóstico de 5 pasos
    ↓
system-coordinator       → Health check del sistema
    ↓
playwright-skill         → Si el fallo es un selector de browser
    ↓
behavioral-modes DEBUG   → Modo debug activo hasta resolver
```

### 🏗️ Mejorar o Expandir Brain OS
```
kaizen                   → Auditoría del sistema actual
    ↓
skill-orchestrator       → ¿Existe ya una skill para lo que falta?
    ↓
elite-skill-architect    → Crear o mejorar la skill necesaria
    ↓
mcp-builder              → Si se necesita una nueva integración
    ↓
workflow-automation      → Diseñar el flujo para que sea robusto
```

---

## ⚡ Referencia Rápida de Triggers

```
ESTUDIO
"Quiero estudiar [X]"              → pomodoro
"Explícame [concepto]"             → behavioral-modes TEACH + notebooklm
"¿Qué dice el libro sobre [X]?"   → notebooklm

TAREAS Y ENTREGAS
"Crea un documento Word"           → docx-official
"Genera la presentación de [X]"   → pptx-official
"Analiza estos datos en Excel"     → xlsx-official
"Escribe el ensayo sobre [X]"      → doc-coauthoring
"Investiga [X] académicamente"     → research-engineer
"¿Qué se dice hoy sobre [X]?"     → last30days

SISTEMA
"Buenos días" / "Empecemos"        → /buenos-dias (boot completo)
"Verifica el sistema"              → system-coordinator
"Sincroniza con Moodle"            → aula-virtual
"Organiza mis archivos"            → file-organizer
"Limpia el sistema"                → cleanup-manager
"Guarda este archivo"              → library-manager

BRAIN OS DEV
"Crea una skill para [X]"          → elite-skill-architect
"¿Qué skill uso para [X]?"         → skill-orchestrator
"Audita Brain OS"                  → kaizen
```

---

*Guía generada el 2026-03-03 | Brain OS v2.1 | 42 skills activas*
