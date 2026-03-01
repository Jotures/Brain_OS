# 🔧 Mejoras Concretas para Brain OS — Basadas en Deep Research

> **Fuente**: 20 archivos de Deep Research procesados (2026-02-12)
> **Prioridad**: Ordenadas por impacto potencial en el rendimiento académico

---

## 🔴 Alta Prioridad (Impacto Inmediato)

### 1. Upgrade del Pomodoro Timer: BRAC 90/20

**Insight fuente**: *Gestión de Energía vs Tiempo* + *Pomodoro Optimizado*

**Estado actual**: El Pomodoro Timer soporta modos `default` (25/5) e `intensive` (50/10).

**Mejora propuesta**: Agregar modo `ultradian` (90/20) basado en ciclos BRAC fisiológicos. Detectar automáticamente qué modo usar según:
- Hora del día + cronotipo del usuario
- Tipo de materia (cognitivamente pesada → 90/20, ligera → 25/5)

**Implementación**:
- Modificar la skill `pomodoro` para soportar un tercer modo
- Agregar campo `cronotipo` a `brain_config.md` (Lion/Bear/Wolf/Dolphin)
- Lógica: si hora está en "peak cognitivo" del cronotipo → sugerir 90/20

---

### 2. Prompts de Active Recall Post-Pomodoro

**Insight fuente**: *Active Recall & Anki* + *Prompting para Estudio*

**Estado actual**: Al terminar un Pomodoro, el sistema solo registra tiempo. No hay intervención pedagógica.

**Mejora propuesta**: Tras cada Pomodoro, Brain OS genera automáticamente 2–3 preguntas de retrieval practice sobre el tema estudiado, usando los prompts Bloom de nivel "Aplicar" o "Analizar".

**Implementación**:
- Integrar prompt templates del archivo *Prompting para Estudio* en la fase de cierre del Pomodoro
- Prompt: `"Genera 3 preguntas de autotest nivel Bloom 3-4 sobre [tema del Pomodoro recién completado]"`
- Opcional: guardar respuestas en Notion como flashcards para spacing posterior

---

### 3. Hemingway Bridge en el Flujo de Cierre

**Insight fuente**: *Second Brain para Estudiantes*

**Estado actual**: El cierre del flujo maestro registra sesión + revisa dudas + actualiza dashboard. Pero **no captura el próximo paso concreto**.

**Mejora propuesta**: Agregar step "Hemingway Bridge" al cierre: preguntar *"¿Con qué oración/idea/problema específico quieres empezar mañana?"* y guardarlo como primera línea del plan del día siguiente.

**Implementación**:
- Nuevo paso en Fase Cierre del Flujo Maestro (paso 11b)
- Guardar en Notion (`BD_TRACKER_DIARIO`) o como campo en `INICIO.md`
- En el próximo Boot, mostrar: *"Ayer dejaste este hilo: [texto del bridge]"*

---

## 🟡 Media Prioridad (Mejoras Estructurales)

### 4. Progressive Summarization en Library Manager

**Insight fuente**: *Second Brain para Estudiantes*

**Estado actual**: `library-manager` mueve archivos y los registra en Notion. No hay procesamiento posterior del contenido.

**Mejora propuesta**: Al registrar un nuevo recurso, auto-generar la "Capa 1" de Progressive Summarization (resumen ejecutivo de 3–5 líneas) usando el LLM. Guardar en la entrada de Notion.

**Implementación**:
- Opción A: Usar el LLM (Antigravity) para leer el PDF y generar resumen
- Opción B: Subir a NotebookLM y pedir el resumen desde ahí
- Almacenar como campo `resumen_auto` en `BD_RECURSOS`

---

### 5. Gamificación: XP por Pomodoros + Streaks Visibles

**Insight fuente**: *Gamificación del Estudio*

**Estado actual**: Existe sistema de rachas en el workflow, pero los Pomodoros no otorgan XP ni hay visualización de progreso gamificado en `INICIO.md`.

**Mejora propuesta**: Implementar sistema de XP simple:
- 1 Pomodoro default = 10 XP
- 1 Pomodoro intensive/ultradian = 20 XP
- Streak diaria visible en dashboard con emoji progresivo (🔥→⚡→💎)
- Goal-Gradient: mostrar % hacia el próximo "nivel" o hito semanal

**Implementación**:
- Agregar campo `xp_total` y `nivel` al tracker diario
- Calcular en el paso de cierre del flujo
- Mostrar en `INICIO.md` como barra de progreso

---

### 6. Macro-Comando `"Buenos días"` (Boot Atómico)

**Insight fuente**: *Flujo Maestro BrainOS + Gestión de Energía*

**Estado actual**: El boot requiere 4 comandos manuales: VER → SYNC → DASH → PLAN.

**Mejora propuesta**: Crear workflow `.agent/workflows/buenos-dias.md` que ejecute los 4 pasos como bloque atómico. El Flujo Maestro ya lo sugiere como "futuro".

**Implementación**:
- Crear el workflow con los 4 pasos encadenados
- Incluir detección de día (LU/MI → boot completo, MA/JU → boot rápido)
- Agregar step de energía: *"¿Nivel de energía? (1=baja, 2=normal, 3=crisis)"*

---

### 7. DAG Curricular como Vista en Notion

**Insight fuente**: *Planificación Multi-Semestre*

**Estado actual**: No existe representación visual de prerequisitos entre cursos.

**Mejora propuesta**: Crear una base de datos `BD_MALLA_CURRICULAR` en Notion con:
- Cada curso como entrada
- Relación `prerequisito_de` entre cursos
- Campos: semestre, créditos, criticidad (betweenness centrality)

**Implementación**:
- Definir el grafo de cursos manualmente (una vez)
- Calcular ruta crítica y mostrar en dashboard
- Usar para la planificación semestral: *"¿Qué cursos debo llevar el próximo semestre?"*

---

## 🟢 Baja Prioridad (Optimización Avanzada)

### 8. Modo Debate con Persona Engineering

**Insight fuente**: *Debates Académicos* + *Prompting para Estudio*

**Mejora**: Crear skill `debate-prep` que use la persona "Devil's Advocate" para preparar argumentos con estructura Toulmin automáticamente.

---

### 9. Audio Overview Scheduling

**Insight fuente**: *NotebookLM Avanzado* + *Gestión de Energía*

**Mejora**: Incluir el scheduling de Audio Overviews en el plan diario: sugerir cuál escuchar durante trayectos o como warm-up, basado en el curso del día.

---

### 10. Captura Automática de Clases

**Insight fuente**: *Captura Automática de Información*

**Mejora**: Investigar viabilidad de grabar clases (con Plaud Note o similar) y transcribir con Whisper para alimentar NotebookLM. **Prerequisito**: resolver consentimiento legal con cada profesor.

---

## Resumen de Impacto

| # | Mejora | Esfuerzo | Impacto |
|---|--------|----------|---------|
| 1 | BRAC 90/20 | Medio | 🔴 Alto |
| 2 | Active Recall Post-Pomodoro | Bajo | 🔴 Alto |
| 3 | Hemingway Bridge | Bajo | 🔴 Alto |
| 4 | Progressive Summarization | Medio | 🟡 Medio |
| 5 | XP + Gamificación | Medio | 🟡 Medio |
| 6 | Macro "Buenos días" | Bajo | 🟡 Medio |
| 7 | DAG Curricular | Alto | 🟡 Medio |
| 8 | Modo Debate | Bajo | 🟢 Bajo |
| 9 | Audio Scheduling | Bajo | 🟢 Bajo |
| 10 | Captura de Clases | Alto | 🟢 Bajo |
