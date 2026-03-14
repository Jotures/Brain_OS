---
name: skill-orchestrator
description: "Orquestador central y buscador de habilidades (skills) de Brain OS. Usa esta skill cuando no estés seguro de qué otra skill utilizar para una tarea, o cuando necesites combinar varias skills, y te enseñará a descubrir dinámicamente el catálogo real instalado en el sistema local."
trigger_conditions:
  - "No sé qué skill usar para [X]"
  - "Combina varias skills para [tarea]"
  - "¿Qué skills tengo disponibles?"
  - "Descubre qué skills pueden hacer [X]"
  - "Orquesta un flujo multi-skill"
usage_constraints: "Solo para descubrimiento y enrutamiento de skills. No ejecuta las skills directamente, solo las identifica y sugiere combinaciones."
category: "Sistema"
parameters:
  task: "Descripción de la tarea para la cual buscar skills (string)"
---

# 🎼 Skill Orchestrator v2.0

> Sistema de enrutamiento y descubrimiento activo de habilidades para Brain OS. No memoriza habilidades falsas, las **descubre en tiempo real**.

## Cuándo Usar Esta Skill

Actívala cuando necesites:
- **Descubrir** qué skills existen instaladas para una tarea específica.
- **Seleccionar** la mejor skill basándote en un contexto ambiguo.
- **Combinar** múltiples skills para un flujo de trabajo complejo.
- **Auditar** si el usuario tiene una herramienta específica instalada.

---

## 1. Flujo de Descubrimiento Dinámico

Como agente de Brain OS, **no debes asumir qué skills existen de memoria**. El catálogo de la V2.0 es dinámico y personalizado. Para saber qué puedes hacer, sigue este flujo:

### PASO 1: Listar el Directorio de Skills
Ejecuta la herramienta `list_dir` en la ruta `/skills/` del proyecto.
*(Nunca uses `ls`, usa siempre la herramienta nativa tuya).*

### PASO 2: Filtrar y Explorar
De la lista obtenida, identifica las 3-4 carpetas (`skills/nombre-skill/`) que suenen más relevantes para tu métrica actual.

### PASO 3: Leer el Frontmatter
Ejecuta `view_file` apuntando a `skills/[nombre-skill]/SKILL.md` (o usa `head` hasta la línea 15) para leer el campo `description` del archivo YAML. La descripción te dirá exactamente cuándo y cómo usar esa skill específica.

### PASO 4: Invocar
Si la skill se ajusta a lo que necesitas, aplica las instrucciones que leíste en su archivo `SKILL.md`.

---

## 2. Categorías Core de Brain OS

Aunque el descubrimiento es dinámico, aquí tienes un mapa conceptual de las categorías reales y principales que **SÍ** existen en este sistema base:

### ⚙️ Gestión del Sistema (Sistema y Metadatos)
- `system-coordinator`: Auditorías y verificación del estado general del OS.
- `dashboard-sync`: Mantiene el `INICIO.md` actualizado.
- `cleanup-manager`: Limpieza de basura, temporales e higiene digital.
- `file-organizer`: Ordena la carpeta de Descargas hacia la Universidad.

### 🏛️ Skills Cognitivos y de Arquitectura
- `elite-skill-architect`: Evalúa, audita y crea otras skills.
- `autonomous-agent-patterns`: Flujos de agentes autónomos y seguridad de permisos.
- `agent-memory-systems`: Context Window y memoria a corto/largo plazo.
- `behavioral-modes`: Estados mentales y modos de operación del agente.

### 📚 Entorno Universitario y Estudio
- `notebooklm`: Interfaz RAG con base de datos NotebookLM.
- `aula-virtual`: Descarga y sincronización de clases de la universidad.
- `pomodoro`: Temporizadores, BRAC y validación de Active Recall.
- `library-manager`: Gestión de lecturas y libros.

### 📝 Trabajo y Planificación Documental
- `planning`, `executing-plans`, `brainstorming`: Ciclo de trabajo metódico.
- `doc-coauthoring`: Trabajo colaborativo en ensayos reflexivos.
- `research-engineer`, `systematic-debugging`: Solución profunda a bugs y teoría.
- `docx-official`, `xlsx-official`, `pdf`, `pptx-official`: Parser y manipulación de ofimática.

---

## 3. Patrones de Combinación (Orquestación)

Para tareas complejas, combina múltiples skills secuencialmente. 

### Caso: Sesión de Estudio Profundo
1. `@system-coordinator` (o `dashboard-sync`) → Verifica qué curso está activo y prepara el dashboard.
2. `@pomodoro` → Inicia un temporizador focalizado.
3. `@aula-virtual` → Comprueba si hay nuevos materiales del curso.
4. `@notebooklm` → Dispara preguntas analíticas guardadas en la BD.
5. Hemingway Bridge (`agent-memory-systems`) → Transición y cierre del bloque.

### Caso: Resolución de Tareas / Ensayos
1. `@brainstorming` → Dibuja en `tmp/` un mapa mental de los requisitos de la tarea.
2. `@doc-coauthoring` → Redacta colaborativamente iterando sección a sección.
3. `@docx-official` → Empaqueta reflexiones finales a un documento `.docx` listo para enviar.

### Caso: Creando o mejorando herramientas de Brain OS
1. `@elite-skill-architect` → Audita la skill para entender brechas (1-100 pts).
2. `@autonomous-agent-patterns` → Para verificar patrones de seguridad y rollback.
3. Edit Tools + `cleanup-manager` → Actualiza el log y limpia el proceso residual.

---

## 4. Resolución de Conflictos

- **Si el usuario invoca una skill que NO encuentras:** No inventes. Responde: *"He procesado tu comando pero, tras listar el directorio `/skills`, no encuentro esa herramienta instalada en Brain OS. ¿Deseas que use `elite-skill-architect` para diseñarla?"*
- **Ambigüedad de funciones:** Si dos skills parecen resolver lo mismo (ej. `brainstorming` y `research-engineer`), recuerda que el primero es para idear antes de tocar código, y el segundo es para investigar en profundidad sobre bases literarias firmes. Lee sus `SKILL.md` para discernir.
