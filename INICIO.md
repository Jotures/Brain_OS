# 🧠 BRAIN OS 2.0 - Panel de Control

> **Semestre**: 2026-1 (Primera semana) | **Meta**: Nota 20 en todos los cursos

---

## 🚀 INICIO RÁPIDO

```
/brain-os-study          → Activa el sistema
"¿Qué debo estudiar?"    → Diagnóstico del día
"Guarda este archivo"    → Ingesta Inteligente 🆕
```

---

## 🧘 VIDA PERSONAL & PROYECTOS

| Proyecto | Estado | Próxima Acción |
|----------|--------|----------------|
| 🇬🇧 Inglés (Máximo) | 🟢 Activo | Repaso Anki |
| 💪 Salud/Gym | ⚪ Pendiente | Definir rutina |
| 🚀 Side Projects | 🟡 Plan | Brainstorming |

> *Usa "Nuevo proyecto personal [nombre]" para agregar uno.*

---

## 📚 BIBLIOTECA & RECURSOS RECIENTES

| Archivo | Curso | Tipo | Link |
|---------|-------|------|------|
| *Esperando sincronización...* | - | - | [Ver en Notion](https://www.notion.so) |
| *Esperando sincronización...* | - | - | - |

> *Di "Sincroniza mi biblioteca" para actualizar esta lista desde Notion.*

---

## 🎮 COMANDOS POR CATEGORÍA

### 🔍 Diagnóstico
| Di esto... | Brain OS hace... |
|------------|------------------|
| "¿Qué debo estudiar hoy?" | Lista prioridades + Pomodoros |
| "Resume mi semana" | Análisis de productividad |
| "¿Cómo voy en [curso]?" | Estado por aporte |
| "Dashboard de aporte [1/2/3]" | Vista del aporte |

### 📚 Estudio
| Di esto... | Brain OS hace... |
|------------|------------------|
| "Modo Crisis para [curso]" | 4+ Pomodoros intensivos |
| "Evalúa mi tema X" | Calcula Pomodoros |
| "Prepárame para exposición" | Estructura + Q&A |
| "Usa skill [nombre] para [tarea]" | Activa skill |

### 📋 Organización
| Di esto... | Brain OS hace... |
|------------|------------------|
| "Nueva tarea: X para Y, entrega Z" | Crea en Notion |
| "Registra material de [curso]" | Guarda en BD_RECURSOS |
| "Registra mi sesión" | Actualiza progreso |

### 🔬 Avanzados
| Di esto... | Brain OS hace... |
|------------|------------------|
| "Consulta mi libro de [curso]" | Query a NotebookLM |
| "Genera resumen de [tema]" | Crea resumen |
| "¿Qué dudas tengo pendientes?" | Lista dudas |
| "Actualiza el dashboard" | Sincroniza INICIO.md |

### 🍅 Pomodoro Timer
| Di esto... | Brain OS hace... |
|------------|------------------|
| "Inicia Pomodoro para [tema]" | Timer adaptativo (auto-modo) |
| "¿Cuánto tiempo me queda?" | Estado del timer |
| "Pausa/Reanuda el timer" | Control de sesión |
| "Detén el Pomodoro" | Detiene y registra |
| "¿Cuántos pomodoros hoy?" | Analytics del día |
| "Mi productividad de la semana" | Analytics semanal |

> **Modos**: `default` (25min) | `intensive` (50min) | `light` (15min) | `exam_prep` (45min)

### 📚 NotebookLM (Conectado ✅)

| Curso | Comando | Estado |
|-------|---------|--------|
| 📗 Economía Ambiental | "Consulta mi libro de Economía Ambiental" | ⏳ |
| 📘 Economía Internacional I | "Consulta mi libro de Economía Internacional" | ⏳ |
| 📙 Economía y Gestión Pública | "Consulta mi libro de Gestión Pública" | ⏳ |
| 📕 Investigación Operativa | "Consulta mi libro de Investigación Operativa" | ⏳ |
| 📔 Teoría Monetaria | "Consulta mi libro de Teoría Monetaria" | ⏳ |
| 📓 Investigación Económica | "Consulta mi libro de Investigación Económica" | ⏳ |
| 📒 Inglés | "Consulta mi libro de Inglés" | ✅ 65 fuentes |

#### 🔄 Flujo Híbrido B+C (Nuevo)
| Di esto... | Brain OS hace... |
|------------|------------------|
| "Prepara contenido para NotebookLM de [curso]" | Genera documento para pegar |
| "Consulta mi libro de [curso]: [pregunta]" | Query grounded a NotebookLM |

### 🌐 Inglés (Curso Personal)

| Herramienta | Comando |
|-------------|---------|
| 📒 NotebookLM | "Consulta mi libro de Inglés" |

### 🎓 Aula Virtual UAndina (Conectado ✅)

| Di esto... | Brain OS hace... |
|------------|------------------|
| "¿Qué tareas tengo pendientes?" | Lista deadlines de Moodle |
| "Tareas de [curso]" | Filtra por curso |
| "Mis notas de [curso]" | Consulta calificaciones |
| "Cursos del aula virtual" | Lista cursos matriculados |
| "Sync tareas a Notion" | Sincroniza con BD_TAREAS |

> 🔴 Urgente (≤2d) | 🟡 Pronto (≤7d) | 🟢 Normal

### 🔗 Ecosistema Integrado (Bidireccional)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Aula Virtual│────▶│  Brain OS   │◀───▶│   Notion    │
│   (Moodle)  │     │  (Central)  │     │ BD_TAREAS   │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │NotebookLM│ │ Pomodoro │ │ Skills   │
       │ (7 books)│ │  Timer   │ │  (28+)   │
       └──────────┘ └──────────┘ └──────────┘
```

| Integración | Estado | Tipo | Flujo |
|-------------|--------|------|-------|
| 📚 NotebookLM | ✅ | Lectura | Consultas → Audio → Q&A |
| 🎓 Aula Virtual | ✅ | Lectura | Tareas → Brain OS |
| 📋 Notion | ✅ | **Bidireccional** | 📥 Lee + 📤 Escribe |
| 🍅 Pomodoro Timer | ✅ | Local | Timer adaptativo + history |
| 🔄 Dashboard | ✅ | Auto-sync | INICIO.md actualizado |

---

## 📊 ESTADO ACTUAL

| Métrica | Valor |
|---------|-------|
| Semestre | 2026-1 |
| Aporte | 1 (en curso) |
| Cursos universidad | 6 |
| Curso personal | 1 (Inglés) |
| Tareas pendientes | 0 ✅ |
| Integraciones | 4 activas |
| Skills | 30 |
| Última verificación | 2026-02-09 00:32 |

---

## 🔗 NAVEGACIÓN RÁPIDA

| Destino | Link |
|---------|------|
| 📚 Mis Cursos | [carrera/semestres/2026-1/cursos/](./carrera/semestres/2026-1/cursos/) |
| 🇬🇧 Inglés | [07_ingles/](./carrera/semestres/2026-1/cursos/07_ingles/) |
| 📈 Resumen Carrera | [carrera/README.md](./carrera/README.md) |
| 📝 Templates | [templates/](./templates/) |
| 📂 Sesiones | [sesiones/](./sesiones/) |
| 🛠️ Skills | [skills/](./skills/) |

---

## 🛠️ SKILLS DISPONIBLES (30)

| Categoria | Skills |
|-----------|--------|
| 📄 Docs | `docx` `xlsx` `pptx` `pdf` |
| ✍️ Escribir | `copywriting` `copy-editing` `content-creator` |
| 📋 Planificar | `brainstorming` `writing-plans` `concise-planning` |
| 🔍 Investigar | `notebooklm` 🔥 `research-engineer` |
| 🎓 Académico | `aula-virtual` |
| 🔄 Sistema | `dashboard-sync` `system-coordinator` 🆕 |

**Uso**: `"Usa la skill [nombre] para [tarea]"`

---

## ⏰ RECORDATORIOS

| Tipo | Cuándo | Símbolo |
|------|--------|---------|
| Crítico | 1 día antes | 🔴 |
| Preparación | 3-5 días | 🟠 |
| Planificación | 7 días | 🟡 |

---

## 📅 PRÓXIMAS TAREAS

> *Sin tareas registradas - Primera semana del semestre*

---

## ⚡ TIPS

- **Primera vez**: Di "¿Qué debo estudiar hoy?" para probar
- **Nuevo material**: Di "Registra material de [curso]"
- **Pre-examen**: Activa "Modo Crisis para [curso]"
- **Dudas**: "Consulta mi libro de [curso]" (requiere NotebookLM)
