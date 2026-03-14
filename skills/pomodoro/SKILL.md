---
name: pomodoro
description: Gestión de temporizador Pomodoro adaptativo para sesiones de estudio. Incluye modo BRAC 90/20, Active Recall post-sesión, y perfiles por materia.
trigger_conditions:
  - "Inicia un Pomodoro"
  - "Sesión de estudio de [materia]"
  - "Modo BRAC 90/20"
  - "Active Recall post-sesión"
  - "¿Cuántos Pomodoros llevo hoy?"
  - "Perfil de estudio para [materia]"
usage_constraints: "Solo para gestión de sesiones de estudio con temporizador. No usar para planificación de estudio (usar planning o study-router) ni para consultas de materiales (usar library-manager o notebooklm)."
category: "Académico"
parameters:
  mode: "Modo: classic-25/5 | brac-90/20 | custom"
  subject: "Materia de estudio (string, opcional)"
---

# 🍅 Pomodoro Timer Skill

## Descripción
Skill para gestionar sesiones de estudio con el temporizador Pomodoro adaptativo de Brain OS. Incluye modo ultradiano BRAC 90/20 para inmersión profunda, Active Recall automático post-sesión, y perfiles adaptativos por materia.

## Cuándo Usar
- Usuario quiere iniciar una sesión de estudio
- Usuario pregunta cuánto tiempo estudiar
- Usuario necesita concentrarse en una tarea específica
- Usuario quiere ver su progreso de pomodoros

## Comandos Disponibles

```powershell
# Ejecutar desde Brain_OS/tools/pomodoro/
python pomodoro_timer.py <comando> [opciones]
```

### Comandos

| Comando | Uso |
|---------|-----|
| `start` | `--topic "Tema" --mode [auto\|default\|intensive\|light\|exam_prep\|ultradian]` |
| `pause` | Sin argumentos |
| `resume` | Sin argumentos |
| `stop` | Sin argumentos |
| `status` | Sin argumentos, retorna JSON |
| `history` | `--period [today\|week\|month]` |
| `suggest` | `--topic "Tema"` |

## Perfiles de Timer

| Perfil | Trabajo | Break | Cuándo |
|--------|---------|-------|--------|
| `default` | 25 min | 5 min | Materias estándar, repaso general |
| `intensive` | 50 min | 10 min | Temas complejos (Cálculo, Física) |
| `light` | 15 min | 3 min | Inglés, repaso rápido, baja energía |
| `exam_prep` | 45 min | 8 min | Preparación de exámenes |
| `ultradian` | 90 min | 20 min | **BRAC fisiológico** — inmersión profunda, escritura, investigación |

## Reglas Adaptativas

El agente DEBE sugerir el modo apropiado según el contexto:

| Tema/Contexto | Modo Sugerido |
|---------------|---------------|
| Inv. Operativa, Simplex, Programación Lineal | `ultradian` (90 min trabajo) |
| Economía Internacional, Comercio, Aranceles | `ultradian` (90 min trabajo) |
| Tesis, Paper, Ensayo largo, Monografía | `ultradian` (90 min trabajo) |
| Cálculo, Física, Álgebra | `intensive` (50 min trabajo) |
| Inglés, Lectura, Repaso | `light` (15 min trabajo) |
| Examen, Parcial, Final | `exam_prep` (45 min trabajo) |
| Econ. Ambiental, Gestión Pública, Teoría Monetaria | `default` (25 min trabajo) |
| Inv. Económica | `default` (25 min trabajo) |
| Otros | `default` (25 min trabajo) |

> **Nota sobre `ultradian`:** Alineado con los ciclos BRAC (Basic Rest-Activity Cycle) de ~90 minutos. Ideal para el usuario que prefiere sesiones largas y pocas. El break de 20 minutos es esencial — caminar, estirarse, NO scrollear.

## Flujo de Uso

1. **Usuario pide estudiar**: Usar `suggest` para obtener modo recomendado
2. **Confirmar e iniciar**: Usar `start` con el modo sugerido
3. **Durante sesión**: Usar `status` si el usuario pregunta tiempo restante
4. **Al terminar**: El timer notifica automáticamente
5. **Active Recall**: Generar 2-3 preguntas post-sesión (ver sección abajo)
6. **Si interrumpe**: Usar `pause` o `stop` según corresponda

## Active Recall Post-Sesión

**Al completar cada sesión de Pomodoro**, el agente DEBE:

1. Generar 2-3 preguntas sobre el tema estudiado (Bloom nivel 3-4: aplicar/analizar)
2. Presentarlas al usuario **antes** del break
3. Evaluar respuesta:
   - ✅ Responde bien → "Comprensión alta" → siguiente tema
   - 🔶 Parcial → Anotar el gap → re-estudiar en próxima sesión
   - ❌ No responde → Repetir el tema en la siguiente ventana

### Plantilla de Active Recall
```
📝 Active Recall — [Tema estudiado]

1. [Pregunta de aplicación: "¿Cómo aplicarías X para resolver Y?"]
2. [Pregunta de análisis: "¿Qué diferencia hay entre X e Y?"]
3. [Pregunta de conexión: "¿Cómo se relaciona X con lo visto en [otro curso]?"]

¿Puedes responder sin mirar apuntes?
```

### Prompts para el Agente (ver `prompt-templates.md`)
- Feynman Check: Para verificar comprensión real
- Devil's Advocate: Para preparar defensas de argumentos
- Chain of Density: Para generar resúmenes densos

## Ejemplo de Interacción

```
Usuario: "Quiero estudiar Investigación Operativa"
Agente: 
1. python pomodoro_timer.py suggest --topic "Investigación Operativa"
   → {"suggested_mode": "ultradian", "work_duration": 90}
2. "Te sugiero modo BRAC 90/20 (90 min trabajo + 20 min descanso).
    Ideal para inmersión profunda en Inv. Operativa. ¿Inicio?"
3. python pomodoro_timer.py start --topic "Investigación Operativa" --mode ultradian
   → Inicia sesión de 90 minutos
4. [Al completar] → Active Recall: 3 preguntas sobre el tema
```

## Integración con Notion

Los pomodoros completados se sincronizan con `BD_TRACKER_DIARIO`:
- Propiedad: `🍅 Pomodoros`
- Tipo: Número
- Se incrementa automáticamente al completar cada ciclo

## Outputs (JSON)

### status
```json
{
  "status": "running",
  "phase": "work",
  "cycle": 2,
  "topic": "Inv. Operativa",
  "mode": "ultradian",
  "remaining": "45:12"
}
```

### history
```json
{
  "period": "today",
  "total_pomodoros": 3,
  "total_focus_minutes": 230,
  "sessions": [
    {"topic": "Inv. Operativa", "mode": "ultradian", "duration": 90},
    {"topic": "Econ. Internacional", "mode": "ultradian", "duration": 90},
    {"topic": "Inglés", "mode": "light", "duration": 15}
  ]
}
```
