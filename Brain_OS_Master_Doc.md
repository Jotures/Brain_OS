# 🧠 Brain OS 2.1: Documentación Maestra

> **Versión del Sistema**: 2.1 — Integración Deep Research (Semestre 2026-1)
> **Objetivo**: Maximizar rendimiento académico (Nota 20) con mínima fricción operativa.
> **Cronotipo**: Bear 🐻 — Peak 10:00-14:00 | Dip 14:00-16:00 | Recovery 16:00-18:00
> **Flujo Maestro**: [v2.0](./Flujo_Maestro_BrainOS_v2.md)

---

## 1. Visión General: El Ecosistema "Brain OS"

**Brain OS** no es solo un conjunto de scripts; es un **Sistema Operativo Cognitivo** que vive dentro del entorno de desarrollo **Antigravity**.

> **¿Qué significa esto?**
> Brain OS es un **Agente de IA (Gemini)** con esteroides, que tiene permiso para ejecutar código en tu computadora local, leer tus archivos y navegar por internet.

### 🏗️ Infraestructura Híbrida

| Capa | Tecnología | Función |
|------|------------|---------|
| **Cerebro (AI)** | **Gemini (via Antigravity)** | Razonamiento, planificación y ejecución de tareas complejas. |
| **Cuerpo (Local)** | **Python + File System** | Ejecución de scripts, almacenamiento de archivos y estructura de carpetas. |
| **Memoria (Nube)** | **Notion + NotebookLM** | Base de datos estructurada y "RAG" (Retrieval-Augmented Generation) para libros. |
| **Sentidos (Input)** | **Moodle API** | Conexión automática con el mundo exterior (Universidad). |

En resumen: **Antigravity es el "cuerpo" donde vive el agente, y Brain OS es la "personalidad" y conjunto de herramientas que hemos construido para él.**

---

## 2. Arquitectura del Sistema

El sistema opera bajo una arquitectura de **Hub Central** donde `Brain_OS` (local) actúa como el cerebro que orquesta servicios externos.

```mermaid
graph TD
    User((Usuario)) <-->|Comandos| BrainOS[🧠 Brain OS (via Antigravity)]
    
    subgraph Nube ["Nube & Servicios"]
        Notion[(Notion DBs)]
        NotebookLM[NotebookLM AI]
        Moodle[Aula Virtual UAndina]
    end
    
    subgraph Core ["Brain OS Core"]
        Coord[System Coordinator]
        Dash[Dashboard INICIO.md]
        Skills[Skills 30+]
    end
    
    BrainOS <--> Coord
    Coord -->|Sincroniza| Dash
    
    %% Integraciones
    BrainOS <-->|Lee/Escribe| Notion
    BrainOS <-->|Consulta/Indexa| NotebookLM
    BrainOS <--|Descarga/Consulta| Moodle
    
    %% Flujos de Datos
    Moodle -->|Tareas/Archivos| BrainOS
    BrainOS -->|Respaldo| Notion
    BrainOS -->|Contexto| NotebookLM
```

### Componentes Principales

1.  **Local (Brain OS)**:
    *   **`INICIO.md`**: El "Head-Up Display" (HUD). Tu panel de control diario.
    *   **`brain_config.md`**: La fuente de verdad. Contiene IDs, rutas y configuraciones.
    *   **`skills/`**: 30+ módulos funcionales (scripts Python) que ejecutan tareas.
    *   **`carrera/`**: Estructura de archivos ordenada por semestres y cursos.

2.  **Integraciones**:
    *   **Notion**: Base de datos persistente (Tareas, Recursos, Diario).
    *   **NotebookLM**: "Cerebro Secundario" para consultas sobre libros y separatas.
    *   **Aula Virtual (Moodle)**: Fuente de input (tareas, fechas, archivos).

---

## 3. Skills Principales (Módulos Funcionales)

El sistema se divide en "Skills" especializadas. Aquí las más críticas:

### 🔗 System Coordinator (`system-coordinator`)
*   **Función**: El "pegamento" del sistema.
*   **Qué hace**: Verifica que todos los IDs de Notion y NotebookLM coincidan. Auto-detecta nuevos cursos y actualiza la documentación.
*   **Comando clave**: `"Verifica el sistema"`, `"Sincroniza todo"`.

### 🔄 Dashboard Sync (`dashboard-sync`)
*   **Función**: Mantener el HUD actualizado.
*   **Qué hace**: Lee el estado actual (pomodoros, tareas, skills) y reescribe `INICIO.md` automáticamente.
*   **Comando clave**: `"Actualiza el dashboard"`.

### 🎓 Aula Virtual (`aula-virtual`)
*   **Función**: Conexión con la universidad.
*   **Qué hace**:
    *   Descarga archivos automáticamente a la carpeta correcta.
    *   Lista tareas pendientes y notas.
    *   Sincroniza deadlines con Notion.
*   **Comando clave**: `"Sincronizar Aula Virtual Completo"`, `"¿Qué tareas tengo?"`.

### 📚 NotebookLM (`notebooklm`)
*   **Función**: Asistente de investigación profundo.
*   **Qué hace**: Permite "chatear" con tus libros y separatas. Usa browser automation para consultar Google NotebookLM y traer respuestas citadas.
*   **Comando clave**: `"Consulta mi libro de [curso]: [pregunta]"`.

### 🍅 Pomodoro Adaptativo (`pomodoro`)
*   **Función**: Gestión de tiempo, foco y retención.
*   **Qué hace**: Inicia timers con duración variable. Incluye modo **BRAC 90/20** (ultradian) para inmersiones profundas, y **Active Recall** automático post-sesión con 3 preguntas Bloom nivel 3-4.
*   **Perfiles**: `default` (25/5), `intensive` (50/10), `light` (15/3), `exam_prep` (45/8), `ultradian` (90/20).
*   **Prompt Templates**: Autotest, Feynman Check, Devil's Advocate, Chain of Density, Socratic Tutor, Exam Simulator.
*   **Comando clave**: `"Inicia Pomodoro para [tema]"` (auto-detecta perfil).

### 📂 Library Manager (`library-manager`)
*   **Función**: Bibliotecario automático + Progressive Summarization.
*   **Qué hace**: Mueve archivos a `carrera/` y los registra en Notion. Soporta **4 capas de Progressive Summarization**: Captura → Negrita → Resaltado → Resumen ejecutivo.
*   **Comando clave**: `"Guarda este archivo"`, `"Resume progresivamente [material]"`.

### ⚙️ Sistema Avanzado (Skills Nuevas v2.1)

| Skill | Función | Complementa |
|-------|---------|-------------|
| `agent-memory-systems` | Arquitectura de memoria del agente: episódica, semántica, procedimental | `system-coordinator` |
| `context-window-management` | Optimización de tokens en sesiones largas (boot, modo crisis) | Todos los flujos |
| `autonomous-agent-patterns` | Patrón del agent loop (Think → Decide → Act → Observe) | `system-coordinator` |
| `skill-orchestrator` | Índice maestro de 240+ skills — descubrimiento y combos | Todos los skills |

### 🛠️ Dev Tools (Skills Nuevas v2.1)

| Skill | Función | Complementa |
|-------|---------|-------------|
| `mcp-builder` | Guía para construir servidores MCP personalizados | `aula-virtual` |
| `personal-tool-builder` | Patrón para crear herramientas CLI | `pomodoro`, `cleanup-manager` |
| `workflow-automation` | Diseño de flujos durables: secuencial, paralelo, orchestrator | Boot diario |

### 🧪 Calidad (Skills Nuevas v2.1)

| Skill | Función | Complementa |
|-------|---------|-------------|
| `systematic-debugging` | Debugging metódico de 5 pasos para scripts del sistema | `system-coordinator` |
| `playwright-skill` | Automatización robusta de browser (Moodle, NotebookLM) | `aula-virtual`, `notebooklm` |

> **Nota**: Cada skill nueva incluye un archivo `BRAIN_OS_CONTEXT.md` que conecta los conceptos genéricos con los módulos reales de Brain OS.

---

## 4. Flujos de Trabajo (Workflows)

### ☀️ Buenos Días (Boot Diario)
Macro-comando atómico: `"Buenos días"` → ejecuta 5 pasos en secuencia:
1.  **Verificar sistema** → `system-coordinator`
2.  **Sincronizar Aula Virtual** → `aula-virtual` (nuevos archivos, tareas, anuncios)
3.  **Actualizar dashboard** → `dashboard-sync`
4.  **Diagnóstico del día** → Notion + prioridades + Pomodoros sugeridos
5.  **Hemingway Bridge** → "Ayer dejaste este hilo: [X]"

*Se adapta al tipo de día: completo (L/MI/VI/S-D) vs simplificado (MA/JU post-clases).*

### 📚 Flujo de Estudio (Selector de Modo)
Al terminar el boot, el usuario elige:
*   📖 **Estudiar** → BRAC 90/20 o Pomodoro + Active Recall post-sesión
*   ✍️ **Escribir ensayo** → Prewriting → Drafting → Revision (Toulmin)
*   🎤 **Preparar expo** → ABT Narrative + Principios de Mayer
*   👥 **Proyecto grupal** → RACI + Sprints semanales
*   🔥 **Modo Crisis** → BRAC 90/20 ×3-4 bloques + interleaving
*   🧘 **Baja energía** → 1 Pomodoro light + Audio Overview pasivo

### 🌉 Cierre Diario (Hemingway Bridge)
1.  **Registrar sesión** → `"Registra mi sesión"`
2.  **Revisar dudas** → `"¿Qué dudas tengo pendientes?"`
3.  **Actualizar dashboard** → `"Actualiza el dashboard"`
4.  **Dejar hilo** → `"Mañana sigo por [X]"` (Hemingway Bridge)

### 📥 Flujo de Ingesta
1.  Descargas un archivo del aula virtual
2.  `"Guarda este archivo en [Curso]"` → archivo en carpeta + Notion
3.  Progressive Summarization: Capa 1 (auto) → Capa 2/3/4 incremental

---

## 5. Estructura de Archivos (El "Cerebro Físico")

```text
Brain_OS/
├── INICIO.md                 # Panel de Control (Dashboard)
├── brain_config.md           # Configuración Maestra
├── carrera/
│   └── semestres/
│       └── 2026-1/           # Semestre Actual
│           ├── cursos/
│           │   ├── 01_economia_ambiental/
│           │   ├── 02_economia_internacional/
│           │   └── ...
│           └── README.md     # Resumen del semestre
├── skills/                   # Scripts y Lógica
│   ├── system-coordinator/
│   ├── notebooklm/
│   ├── aula-virtual/
│   └── ...
└── config/
    └── notebooklm_registry.json # Mapeo de Notebooks
```

---

## 6. Guía Rápida de Comandos

| Categoría | Comando | Acción |
|-----------|---------|--------|
| **Sistema** | `"Verifica el sistema"` | Chequeo de salud y links rotos. |
| | `"Actualiza el dashboard"` | Refresca la vista de `INICIO.md`. |
| **Estudio** | `"¿Qué debo estudiar?"` | Plan de acción del día. |
| | `"Inicia Pomodoro"` | Arranca timer adaptativo. |
| **Investigación** | `"Consulta mi libro de [X]"` | Pregunta a la IA sobre bibliografía. |
| **Gestión** | `"Tareas de [Curso]"` | Lista deadlines desde Moodle. |
| | `"Guarda este archivo"` | Organiza archivos descargados. |

---

## 7. Mantenimiento y Solución de Problemas

*   **¿IDs desincronizados?**: Si Notion o NotebookLM no responden, ejecuta `"Verifica el sistema"`. El coordinador te dirá qué ID falta en `brain_config.md`.
*   **¿Dashboard desactualizado?**: Ejecuta `"Actualiza el dashboard"`.
*   **¿Nuevo curso?**: Usa `"Agrega [nombre curso] al sistema"`. El coordinador creará las carpetas y pedirá los IDs necesarios.
