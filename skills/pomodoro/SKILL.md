---
name: pomodoro
description: Gestión de temporizador Pomodoro adaptativo para sesiones de estudio
---

# 🍅 Pomodoro Timer Skill

## Descripción
Skill para gestionar sesiones de estudio con el temporizador Pomodoro adaptativo de Brain OS.

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
| `start` | `--topic "Tema" --mode [auto\|default\|intensive\|light\|exam_prep]` |
| `pause` | Sin argumentos |
| `resume` | Sin argumentos |
| `stop` | Sin argumentos |
| `status` | Sin argumentos, retorna JSON |
| `history` | `--period [today\|week\|month]` |
| `suggest` | `--topic "Tema"` |

## Reglas Adaptativas

El agente DEBE sugerir el modo apropiado según el contexto:

| Tema/Contexto | Modo Sugerido |
|---------------|---------------|
| Cálculo, Física, Álgebra | `intensive` (50 min trabajo) |
| Inglés, Lectura, Repaso | `light` (15 min trabajo) |
| Examen, Parcial, Final | `exam_prep` (45 min trabajo) |
| Otros | `default` (25 min trabajo) |

## Flujo de Uso

1. **Usuario pide estudiar**: Usar `suggest` para obtener modo recomendado
2. **Confirmar e iniciar**: Usar `start` con el modo sugerido
3. **Durante sesión**: Usar `status` si el usuario pregunta tiempo restante
4. **Al terminar**: El timer notifica automáticamente
5. **Si interrumpe**: Usar `pause` o `stop` según corresponda

## Ejemplo de Interacción

```
Usuario: "Quiero estudiar integrales"
Agente: 
1. python pomodoro_timer.py suggest --topic "Cálculo - Integrales"
   → {"suggested_mode": "intensive", "work_duration": 50}
2. python pomodoro_timer.py start --topic "Cálculo - Integrales" --mode intensive
   → Inicia sesión de 50 minutos
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
  "topic": "Cálculo",
  "remaining": "15:42"
}
```

### history
```json
{
  "period": "today",
  "total_pomodoros": 6,
  "total_focus_minutes": 150
}
```
