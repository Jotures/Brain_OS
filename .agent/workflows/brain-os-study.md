---
description: Sistema Brain OS 2.0 para maximizar rendimiento académico multi-semestre. Activa cuando el usuario quiera estudiar, planificar, recibir recordatorios, o gestionar su carrera.
---

# 🧠 Brain OS 2.0 Study Workflow

Sistema de IA académico multi-semestre para lograr nota 20 en todos los cursos.

---

## Arquitectura Multi-Semestre

```yaml
Ubicación de cursos: carrera/semestres/[SEMESTRE]/cursos/
Semestre actual: 2026-1
```

### Cursos del Semestre 2026-1
| Curso | Tipo | NotebookLM | Notion ID |
|-------|------|------------|-----------|
| Economía Ambiental | Teórico-Proyectos | 📗 Libro 1 | `2fdaacd6-8210-81ae-bffe-f00d7ebaf358` |
| Economía Internacional I | Teórico-Matemático | 📘 Libro 2 | `2fdaacd6-8210-8176-95da-f8f559269cc1` |
| Economía y Gestión Pública | Exposiciones-Ensayos | 📙 Libro 3 | `2fdaacd6-8210-81a1-91d1-ce49066ad036` |
| Investigación Operativa | Matemático-Práctico | 📕 Libro 4 | `2fdaacd6-8210-8133-9234-c6de69555825` |
| Teoría Monetaria y Bancaria | Teórico-Análisis | 📔 Libro 5 | `2fdaacd6-8210-8108-bb2a-ef7bba8a5825` |
| Investigación Económica | Papers-Investigación | 📓 Libro 6 | `2fdaacd6-8210-8143-8a86-f17fd377fe70` |
| Inglés | Práctica-Conversación | 📒 Libro 7 | `2fdaacd6-8210-8134-aa64-df39374251ed` |

---

## Sistema de 3 Aportes

| Aporte | Periodo | Peso | Descripción |
|--------|---------|------|-------------|
| **Aporte 1** | Semanas 1-5 | 30% | Fundamentos del curso |
| **Aporte 2** | Semanas 6-10 | 35% | Desarrollo y profundización |
| **Aporte 3** | Semanas 11-16 | 35% | Evaluación final |

### Campos en BD_TAREAS_MAESTRAS
```yaml
Tarea: "Nombre de la tarea"
Tipo: 📅 Evento | 🚧 Proyecto | ⚡ Examen | 📝 Tarea
Aporte: Aporte 1 | Aporte 2 | Aporte 3
Fecha Entrega: [Deadline]
Peso: [% del aporte]
Área/Curso: [Relación a BD_AREAS]
Estado: Por hacer | En progreso | Listo
Prioridad: 🔥 Alta | ⚡ Media | ☁️ Baja
```

---

## ⏰ Sistema de Recordatorios Automáticos

### Tipos de Alerta
| Tipo | Tiempo | Acción del Sistema |
|------|--------|-------------------|
| 🔴 **CRÍTICO** | 1 día antes | "¡MAÑANA: [Tarea]!" |
| 🟠 **PREPARACIÓN** | 3-5 días | "Inicia repaso para [Tarea]" |
| 🟡 **PLANIFICACIÓN** | 7 días | "Crea plan de estudio para [Tarea]" |
| 🟢 **NUEVO TEMA** | Inicio de unidad | "Nuevo tema disponible" |

### Lógica de Recordatorios
// turbo
```
1. Consultar BD_TAREAS_MAESTRAS → Deadlines próximos
2. Calcular días restantes con fórmula "Días Restantes"
3. Generar alerta según tipo:
   - Si días <= 1 → 🔴 Crítico
   - Si días <= 5 → 🟠 Preparación
   - Si días <= 7 → 🟡 Planificación
4. Sugerir Pomodoros necesarios
```

---

## Integración Notion MCP

### IDs de Bases de Datos STUDENT OS
```yaml
# Página Principal
STUDENT_OS_PAGE: "2cbaacd6-8210-8026-8123-c3e2ea77b09e"

# Bases de Datos Centrales
BD_AREAS: "2cbaacd6-8210-803e-8df2-d2d5b84232c2"
BD_TAREAS_MAESTRAS: "2cbaacd6-8210-803b-b9d9-d78fa3066b2a"
BD_RECURSOS: "2cbaacd6-8210-80ea-9bff-d7aa9ffe3c41"

# Vistas en Página Principal
DB_SEMESTRE: "2d3aacd6-8210-8077-9c39-fb3604600f64"
DB_EN_FOCO: "2d3aacd6-8210-80dd-8f84-c63c7192992e"
DB_RACHA: "2cbaacd6-8210-807b-8e7b-f39c0655b059"
```

### Operaciones Disponibles
// turbo
```
1. Consultar BD_TAREAS_MAESTRAS → Ver tareas pendientes
2. Consultar DB_SEMESTRE → Ver cursos activos
3. Actualizar DB_RACHA → Registrar progreso diario
4. Crear en BD_RECURSOS → Agregar materiales de estudio
```

---

## Algoritmo de Pomodoros Adaptativos

### 🍅 Pomodoro Timer (tools/pomodoro/)

El sistema cuenta con un temporizador adaptativo que ajusta automáticamente las duraciones:

| Modo | Trabajo | Descanso | Detectado por |
|------|---------|----------|---------------|
| `default` | 25 min | 5 min | General |
| `intensive` | 50 min | 10 min | Cálculo, Física, Álgebra |
| `light` | 15 min | 3 min | Inglés, Lectura, Repaso |
| `exam_prep` | 45 min | 8 min | Examen, Parcial, Final |
| `ultradian` | 90 min | 20 min | Inv. Operativa, Econ. Internacional, Tesis, Papers |

#### Comandos del Timer
```powershell
# Desde Brain_OS/tools/pomodoro/
python pomodoro_timer.py start --topic "[Tema]"     # Auto-detecta modo
python pomodoro_timer.py status                      # Ver tiempo restante
python pomodoro_timer.py pause | resume | stop       # Control
python pomodoro_timer.py history --period week       # Analytics
```

### Evaluación de Dificultad
Antes de cada sesión de estudio, Brain OS evalúa:

```
1. ¿El tema es nuevo o ya lo he visto?
   - Nuevo → +1 Pomodoro
   - Revisión → Base

2. ¿Involucra matemáticas/modelos complejos?
   - Sí (ej: Investigación Operativa) → Modo ultradian o intensive
   - No → Modo default/light

3. ¿Hay deadline en los próximos 3 días?
   - Sí → Modo exam_prep (+2 Pomodoros)
   - No → Normal

4. ¿Es para exposición o examen?
   - Exposición → +1 (tiempo de práctica oral)
   - Examen → +1 (tiempo de Active Recall)
```

### Tabla de Asignación
| Situación | Modo | Pomodoros | Duración Total |
|-----------|------|-----------|----------------|
| Repaso simple | `light` | 1 | 15 min |
| Tema nuevo fácil | `default` | 2 | 50 min |
| Tema nuevo difícil | `intensive` | 2 | 100 min |
| Inmersión profunda (Inv. Op, Econ. Inter) | `ultradian` | 1-2 | 90-180 min |
| Pre-examen/exposición | `exam_prep` | 3 | 135 min |
| Modo Crisis | `ultradian` | 3+ | 270+ min |

---

## Flujo de Trabajo Diario

### Paso 1: Diagnóstico Matutino
// turbo
```
1. Consultar Notion (MCP) → Obtener deadlines de los próximos 7 días
2. Identificar prioridades del día
3. Calcular Pomodoros necesarios
```

### Paso 2: Sesión de Estudio
Para cada tema a estudiar:

1. **Preparación** (2 min)
   - Abrir materiales en NotebookLM
   - Cerrar distracciones

2. **Active Recall** (durante Pomodoro)
   - Usar técnica Feynman: Explicar el concepto como si enseñaras a alguien
   - Crear analogías físicas:
     - Elasticidad → Banda elástica
     - Curva IS-LM → Bañera con fuga
     - Equilibrio Nash → Semáforo de tráfico

3. **Consolidación** (5 min post-Pomodoro)
   - Anotar dudas en Notion
   - Marcar progreso

### Paso 3: Registro de Progreso
// turbo
```
Actualizar Notion con:
- Tema estudiado
- Pomodoros completados
- Nivel de comprensión (1-5)
- Dudas pendientes
```

---

## Técnicas por Tipo de Evaluación

### Para Exámenes
1. **Spaced Repetition**: Revisar tema día 1, día 3, día 7
2. **Practice Testing**: Hacer preguntas antes de leer
3. **Interleaving**: Mezclar temas en una sesión

### Para Exposiciones
1. **Estructura 10-20-30**: Max 10 slides, 20 min, font 30pt
2. **Práctica oral**: Grabarse explicando
3. **Anticipar Q&A**: Preparar 5 preguntas difíciles

### Para Proyectos Grupales
1. **Delegación clara**: Definir responsables
2. **Checkpoints semanales**: Revisar avance
3. **Buffer de tiempo**: Terminar 2 días antes

### Para Papers/Investigación
1. **Lectura efectiva**: SQ3R (Survey, Question, Read, Recite, Review)
2. **Gestión de citas**: Organizar fuentes desde el inicio
3. **Escritura en bloques**: Introducción → Cuerpo → Conclusión

---

## Comandos del Brain OS 2.0

### Comandos de Diagnóstico
| Comando | Acción |
|---------|--------|
| "¿Qué debo estudiar hoy?" | Consultar Notion → Prioridades con Pomodoros |
| "Resume mi semana" | Análisis de productividad semanal |
| "¿Cómo voy en [curso]?" | Estado del curso por aporte |
| "Dashboard de aporte [1/2/3]" | Vista general del aporte actual |

### Comandos de Estudio
| Comando | Acción |
|---------|--------|
| "Modo Crisis para [curso]" | Sesión intensiva 4+ Pomodoros |
| "Prepárame para exposición de [tema]" | Generar estructura + Q&A |
| "Evalúa mi tema X" | Calcular Pomodoros necesarios |
| "Usa la skill [nombre] para [tarea]" | Activar skill específica |

### Comandos de Organización
| Comando | Acción |
|---------|--------|
| "Nueva tarea: [nombre] para [curso], entrega [fecha]" | Crear tarea en Notion |
| "Registra material de [curso]: [archivo]" | Agregar a BD_RECURSOS |
| "Registra mi sesión" | Guardar progreso en Notion |

### Comandos de Aula Virtual
| Comando | Acción |
|---------|--------|
| "Material nuevo de [curso]" | Registrar descarga del aula |
| "Subir sílabo de [curso]" | Preparar para NotebookLM |

### Comandos NotebookLM Studio v2
| Comando | Acción |
|---------|--------|
| "Consulta mi libro de [curso]: [pregunta]" | Query grounded via HTTP v2 |
| "Genera quiz de [curso]" | Active Recall post-sesión |
| "Genera flashcards de [curso]" | Tarjetas para Spaced Repetition |
| "Genera audio de [curso]" | Audio Overview para repaso pasivo |
| "Genera guía de estudio de [curso]" | Study Guide completa |
| "Genera presentación de [curso]" | Slide Deck .pptx |
| "Genera infografía de [curso]" | Visual conceptual PNG |
| "Genera mapa mental de [curso]" | Mind Map JSON |

### Comandos Pomodoro Timer 🍅
| Comando | Acción |
|---------|--------|
| "Inicia Pomodoro para [tema]" | `python pomodoro_timer.py start --topic "[tema]"` |
| "Pausa el timer" | `python pomodoro_timer.py pause` |
| "¿Cuánto tiempo me queda?" | `python pomodoro_timer.py status` |
| "Detén el Pomodoro" | `python pomodoro_timer.py stop` |
| "¿Cuántos pomodoros llevo hoy?" | `python pomodoro_timer.py history --period today` |
| "Mi productividad de la semana" | `python pomodoro_timer.py history --period week` |

---

## 📚 Flujo NotebookLM v2 (Motor HTTP Directo)

> **Motor Primario:** `notebooklm-py` (HTTP directo, ~10× más rápido)
> **Fallback:** Patchright browser automation (si v2 falla)

### Arquitectura v2
```
Brain OS → notebooklm_client.py → API Google (HTTP) → Respuesta grounded
```

### Comandos de Consulta
```bash
# Query grounded (usar durante estudio para resolver dudas)
python scripts/run.py ask_question_v2.py --notebook-id economia-ambiental --question "¿Cuál es el principio contaminador-pagador?"
```

### Comandos de Active Recall (POST-SESIÓN)
```bash
# Generar quiz después de una sesión (Active Recall automático)
python scripts/run.py generate_quiz.py --notebook-id economia-ambiental --difficulty medium --output quiz_sesion.md

# Generar flashcards para repasos
python scripts/run.py generate_flashcards.py --notebook-id economia-internacional-i --difficulty hard --output flashcards.md
```

### Comandos de Recursos de Estudio
```bash
# Audio Overview para repaso pasivo (mientras caminas, en clase)
python scripts/run.py download_audio.py --notebook-id economia-ambiental --output repaso_ambiental.mp3

# Study Guide completa del tema
python scripts/run.py generate_report.py --notebook-id economia-ambiental --type study_guide --output guia_ambiental.md

# Briefing Doc para exámenes rápidos
python scripts/run.py generate_report.py --notebook-id economia-internacional-i --type briefing_doc --output briefing_econ_int.md

# Infografía para visualizar conceptos
python scripts/run.py generate_infographic.py --notebook-id investigacion-operativa --output infografia_io.png

# Mapa mental de conceptos del tema
python scripts/run.py generate_mind_map.py --notebook-id economia-ambiental --output mapa.json

# Para exposiciones: Slide Deck generado por IA
python scripts/run.py generate_slide_deck.py --notebook-id economia-gestion-publica --output slides_gestion.pptx
```

### Integración en el Flujo de Estudio

| Momento | Herramienta v2 | Propósito |
|---------|---------------|----------|
| Pre-sesión | `generate_report.py --type briefing_doc` | Orientarse rápido |
| Durante | `ask_question_v2.py` | Resolver dudas al instante |
| Post-sesión | `generate_quiz.py` | Active Recall estructurado |
| Post-sesión | `generate_flashcards.py` | Spaced repetition |
| Repaso pasivo | `download_audio.py` | Escuchar mientras se descansa |
| Pre-examen | `generate_report.py --type study_guide` | Guía completa |
| Exposición | `generate_slide_deck.py` | Presentación base |

### Cursos con Notebook Activo
| Curso | Notebook ID | Estado | v2 |
|-------|-------------|--------|----|
| Economía Ambiental | `economia-ambiental` | Activo | ✅ |
| Economía Internacional | `economia-internacional-i` | Activo | ✅ |
| Economía y Gestión | `economia-gestion-publica` | Activo | ✅ |
| Investigación Operativa | `investigacion-operativa` | Activo | ✅ |
| Teoría Monetaria | `teoria-monetaria` | Activo | ✅ |
| Investigación Económica | `investigacion-economica` | Activo | ✅ |
| Inglés | `ingles` | Activo | ✅ |

---

## Integración con Herramientas

### Notion (via MCP)
- Leer/escribir en bases de datos STUDENT OS
- Consultar calendario de deadlines
- Registrar progreso automático

### NotebookLM v2 (Motor HTTP directo)
- 1 Notebook por curso con materiales del sílabo
- **Query durante estudio:** `ask_question_v2.py` (sin browser, instantáneo)
- **Active Recall post-sesión:** `generate_quiz.py` + `generate_flashcards.py`
- **Repaso pasivo:** `download_audio.py` (Audio Overview como mp3)
- **Pre-examen:** `generate_report.py --type study_guide`
- **Exposiciones:** `generate_slide_deck.py`
- **Visualización:** `generate_infographic.py` + `generate_mind_map.py`

### Deep Research
- Investigar temas complejos cuando sea necesario
- Generar contexto adicional para papers

---

## Sistema de Rachas

| Racha | Recompensa |
|-------|------------|
| 7 días consecutivos | 🏆 Badge "Semana Perfecta" |
| 14 días | 🌟 Unlock: Día de descanso libre |
| 30 días | 💎 Meta cumplida del mes |

---

## 📚 Skills Disponibles (24 académicas)

Brain OS tiene acceso a skills curadas en `skills/`:

### Skills Académicas Clave
| Skill | Uso |
|-------|-----|
| `notebooklm` | Consultar libros de NotebookLM directamente desde Antigravity |
| `brainstorming` | Diseñar trabajos/proyectos antes de implementar |
| `writing-plans` | Crear planes de estudio estructurados |
| `research-engineer` | Investigación profunda de temas |
| `concise-planning` | Planificación rápida y efectiva |
| `architecture` | Diseño de proyectos complejos |

### Skills de Productividad
| Skill | Uso |
|-------|-----|
| `executing-plans` | Ejecutar planes paso a paso |
| `plan-writing` | Escribir planes detallados |
| `kaizen` | Mejora continua de tu método |

### Skills de Escritura
| Skill | Uso |
|-------|-----|
| `copywriting` | Redacción persuasiva |
| `copy-editing` | Edición de textos académicos |
| `doc-coauthoring` | Co-escritura de documentos |

### Cómo Usar una Skill
```
"Usa la skill [nombre-de-skill] para [tarea]"
Ejemplo: "Usa la skill brainstorming para diseñar mi proyecto de Economía Ambiental"
```

---

## Notas de Implementación

- Este workflow se activa cuando el usuario menciona estudio, tareas, exámenes o cursos
- Los comandos `// turbo` indican pasos que pueden auto-ejecutarse
- Brain OS debe ser proactivo: si detecta deadline cercano, alertar al usuario
- Usar Output Factory (skill) para sesiones de máxima productividad
