---
name: study-router
description: "Enrutador inteligente de estudio que decide QUE, CUANDO y COMO estudiar. Combina Notion (memoria estructurada) para priorización y NotebookLM (RAG semántico) para contenido. Reemplaza la lógica dispersa en system-coordinator. Usar cuando el usuario diga '¿Qué debo estudiar?', '¿Qué tengo pendiente?', 'Planifica mi estudio', 'Modo Crisis [materia]', '¿Cómo estudio [tema]?'."
trigger_conditions:
  - "¿Qué debo estudiar?"
  - "¿Qué tengo pendiente esta semana?"
  - "Planifica mi estudio para hoy"
  - "Modo Crisis [materia]"
  - "¿Cómo estudio [tema]?"
  - "Prepárame para el examen de [materia]"
usage_constraints: "Solo para decisiones de estudio y enrutamiento entre fuentes. No ejecuta el estudio (usar pomodoro). No consulta directamente Notion o NotebookLM (los invoca como sub-skills)."
category: "Académico"
parameters:
  query: "Pregunta o necesidad de estudio (string)"
  mode: "Modo: what-to-study | how-to-study | crisis | hybrid (inferido del comando)"
---

# 🧭 Study Router

> Enrutador inteligente que responde a "¿Qué debo estudiar?" combinando datos estructurados (Notion) con contenido semántico (NotebookLM).

## Problema que Resuelve

Antes de esta skill, la lógica de enrutamiento de estudio estaba dispersa en `system-coordinator` y dependía de decisiones ad-hoc del agente. El Study Router codifica el **arbol de decision** como un flujo explícito y repetible.

---

## Arbol de Decision

```
Usuario: "¿Qué debo estudiar?" / "Planifica mi estudio" / "Modo Crisis [X]"
                    |
        ┌───────────┼───────────┐
        v           v           v
   RAMA NOTION  RAMA NLML   RAMA HIBRIDA
   (QUE/CUANDO) (COMO)     (QUE + COMO)
```

---

## Rama 1: Notion (Memoria Estructurada)

> **Responde a: QUE estudiar y CUANDO**

### Cuando Usar
- El usuario pregunta por prioridades: "¿Qué debo estudiar?"
- Necesita fechas, urgencia o estado de tareas
- Planificación semanal o diaria de estudio

### Flujo

```
PASO 1 → Consultar Notion (BD_TAREAS / BD_EXAMENES)
  - Filtrar por: fecha_entrega proxima, estado != completado
  - Ordenar por: urgencia (fecha mas cercana primero)

PASO 2 → Clasificar
  - URGENTE (< 48h): Prioridad absoluta
  - PROXIMO (48h - 7d): Planificar esta semana
  - FUTURO (> 7d): Backlog, no priorizar ahora

PASO 3 → Presentar al usuario
  Formato:
  | Prioridad | Materia | Tarea/Examen | Fecha | Estado |
  |-----------|---------|--------------|-------|--------|
  | URGENTE   | ...     | ...          | ...   | ...    |

PASO 4 → Ofrecer siguiente paso
  "¿Quieres que prepare material de estudio para [materia más urgente]?"
  → Si acepta: escalar a Rama Hibrida
```

### Datos que Consulta
- `BD_TAREAS` en Notion: tareas pendientes con fechas
- `BD_EXAMENES` en Notion: examenes programados
- Aula Virtual (via skill `aula-virtual`): tareas de Moodle no sincronizadas

---

## Rama 2: NotebookLM (RAG Semantico)

> **Responde a: COMO estudiar un tema**

### Cuando Usar
- El usuario ya sabe QUE estudiar y necesita CONTENIDO
- Pide preguntas de examen, resúmenes, o explicaciones
- "¿Cómo estudio [tema]?"

### Flujo

```
PASO 1 → Identificar notebook relevante
  - Buscar en biblioteca de NotebookLM el notebook de la materia
  - Si no existe: sugerir crear uno con materiales de 03_Notas/

PASO 2 → Modo de estudio (elegir segun contexto)
  A. INTERROGADOR: Generar 10 preguntas tipo examen desde las fuentes
  B. RESUMIDOR: Extraer conceptos clave y relaciones
  C. EXPLICADOR: Explicar un concepto específico con citaciones

PASO 3 → Ejecutar consulta via skill notebooklm
  - Usar Motor v2 (HTTP) con fallback a Motor v1 (Browser)
  - Entregar respuesta con citaciones de las fuentes

PASO 4 → Post-estudio
  - Sugerir Active Recall: "¿Puedes responder estas 3 preguntas sin ver las notas?"
  - Si el usuario quiere sesion formal → escalar a skill pomodoro
```

### Modos de Consulta

| Modo | Trigger | Prompt a NotebookLM |
|------|---------|---------------------|
| Interrogador | "Prepárame para el examen" | "Genera 10 preguntas tipo examen sobre [tema] basadas en las fuentes" |
| Resumidor | "Resúmeme [tema]" | "Resume los conceptos clave de [tema] con estructura jerárquica" |
| Explicador | "Explícame [concepto]" | "Explica [concepto] citando las fuentes relevantes" |

---

## Rama 3: Hibrida (Notion + NotebookLM)

> **Notion define el QUE → NotebookLM entrega el COMO**

### Cuando Usar
- Modo Crisis (examen inminente)
- "Planifica mi estudio completo para [materia]"
- Cuando Rama 1 identifica urgencias y el usuario quiere actuar

### Flujo

```
PASO 1 → [RAMA NOTION] Identificar materia + tema urgente
  - Consultar BD_EXAMENES → fecha mas cercana
  - Extraer: materia, temas del examen, materiales disponibles

PASO 2 → [RAMA NOTEBOOKLM] Preparar contenido de estudio
  - Localizar notebook de la materia
  - Ejecutar modo INTERROGADOR (preguntas tipo examen)
  - Si hay tiempo: ejecutar modo RESUMIDOR también

PASO 3 → Generar Plan de Estudio
  Formato:
  ┌─────────────────────────────────────────┐
  │  PLAN DE ESTUDIO: [Materia]             │
  │  Examen: [fecha]  |  Tiempo: [X dias]   │
  ├─────────────────────────────────────────┤
  │  1. [Tema] — Prioridad: ALTA            │
  │     Material: [notebook/notas]           │
  │     Acción: Revisar resumen + 10 preguntas│
  │  2. [Tema] — Prioridad: MEDIA           │
  │     Material: [notebook/notas]           │
  │     Acción: Leer conceptos clave         │
  └─────────────────────────────────────────┘

PASO 4 → Ofrecer ejecución
  "¿Iniciamos una sesión Pomodoro con [tema 1]?"
  → Si acepta: escalar a skill pomodoro con perfil de la materia
```

---

## Modo Crisis

> **Patron Secuencial**: Agente Síntesis → Agente Evaluador

El Modo Crisis es un caso especial de la Rama Hibrida con presión de tiempo. Se activa con:
- "Modo Crisis [materia]"
- Examen en < 24h detectado por Rama Notion

### Flujo Secuencial (2 Agentes)

```
AGENTE 1: SINTESIS (research-engineer)
  Input: Notas de 03_Notas/ + PDFs de la materia
  Proceso: Procesar y comprimir en resumen estructurado
  Output: Resumen de 1-2 páginas con conceptos clave,
          definiciones, fórmulas, y relaciones

         ↓ (solo el resumen pasa al siguiente agente)

AGENTE 2: EVALUADOR (notebooklm o agente directo)
  Input: SOLO el resumen estructurado del Agente 1
  Proceso: Generar examen de prueba basado en el resumen
  Output: 10 preguntas tipo examen + respuestas esperadas
          (formato: pregunta, opciones si aplica, respuesta correcta, justificación)
```

### Reglas del Modo Crisis
1. **Contexto aislado**: El Agente 2 recibe SOLO el resumen, no las fuentes originales. Esto previene context rot y fuerza síntesis.
2. **Tiempo limitado**: El flujo completo no debe exceder 1 Pomodoro (25 min).
3. **Output actionable**: El resultado final son preguntas de práctica, no más resúmenes.
4. **Escalamiento**: Si el usuario falla >50% de las preguntas → sugerir sesión de repaso con Rama NotebookLM (modo Explicador).

---

## Integracion con Otras Skills

| Skill | Relacion con Study Router |
|-------|---------------------------|
| `aula-virtual` | Fuente de datos para Rama Notion (tareas de Moodle) |
| `notebooklm` | Motor de consulta para Rama NotebookLM |
| `research-engineer` | Agente Sintesis en Modo Crisis |
| `pomodoro` | Ejecutor de sesiones de estudio post-routing |
| `library-manager` | Consulta de materiales disponibles por curso |
| `system-coordinator` | Study Router reemplaza la logica de estudio dispersa aqui |

---

## Comandos

| Comando | Rama | Descripcion |
|---------|------|-------------|
| "¿Qué debo estudiar?" | Notion | Lista prioridades por urgencia |
| "¿Qué tengo pendiente esta semana?" | Notion | Filtro semanal de tareas/exámenes |
| "¿Cómo estudio [tema]?" | NotebookLM | Contenido de estudio semantico |
| "Prepárame para el examen de [materia]" | Hibrida | Plan completo: prioridades + contenido |
| "Modo Crisis [materia]" | Hibrida (Crisis) | Flujo secuencial sintesis + evaluacion |
| "Planifica mi estudio para hoy" | Hibrida | Plan diario basado en urgencias |

---

## Archivos de la Skill

```
skills/study-router/
└── SKILL.md    ← Este archivo
```

---

## Escenarios de Prueba

### Test 1: Ruta Notion basica

```
Input:    "¿Qué debo estudiar?"
Espera:   Tabla de prioridades desde Notion (BD_TAREAS + BD_EXAMENES)
Verifica: - Ordenado por urgencia (fecha más cercana primero)
          - Clasificación URGENTE/PROXIMO/FUTURO correcta
          - Ofrece escalar a Rama Hibrida
Output:   Tabla + "¿Quieres que prepare material para [materia]?"
```

### Test 2: Ruta NotebookLM

```
Input:    "¿Cómo estudio Economía Internacional?"
Espera:   Consulta al notebook de Economía Internacional
Verifica: - Identifica el notebook correcto
          - Usa modo Interrogador o Resumidor según contexto
          - Respuesta incluye citaciones de fuentes
Output:   Contenido de estudio con citaciones
```

### Test 3: Ruta Hibrida

```
Input:    "Prepárame para el examen de Economía Internacional"
Espera:   Plan completo: Notion (urgencia) + NotebookLM (contenido)
Verifica: - Identifica fecha del examen desde Notion
          - Genera plan con temas priorizados
          - Incluye preguntas de práctica desde NotebookLM
Output:   Plan de estudio estructurado + preguntas de práctica
```

### Test 4: Modo Crisis secuencial

```
Input:    "Modo Crisis Economía Internacional"
Espera:   Flujo de 2 agentes: Síntesis → Evaluador
Verifica: - Agente 1 genera resumen de 03_Notas/ y PDFs
          - Agente 2 recibe SOLO el resumen (no fuentes originales)
          - Output final son preguntas de examen
          - Flujo completo < 25 min
Output:   10 preguntas tipo examen + respuestas + justificaciones
```
