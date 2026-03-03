# 🕹️ Autonomous Agent Patterns — Contexto Brain OS

## Agent Loop de Brain OS

El ciclo Think → Decide → Act → Observe se ejecuta en cada interacción:

```
Think:   Leer estado del sistema (brain_config, INICIO.md, Notion)
Decide:  Priorizar por urgencia × importancia (deadlines + peso de aporte)
Act:     Ejecutar skill correspondiente (pomodoro, aula-virtual, etc.)
Observe: Actualizar dashboard + registrar sesión
```

## Mapeo al Boot Diario (5 pasos)

| Paso Boot | Fase del Loop | Skill |
|-----------|--------------|-------|
| 1. Verificar sistema | Observe | `system-coordinator` |
| 2. Sincronizar Aula | Act | `aula-virtual` |
| 3. Actualizar dashboard | Observe | `dashboard-sync` |
| 4. Diagnóstico del día | Think + Decide | Notion queries |
| 5. Hemingway Bridge | Think | Lectura de `sesiones/` |

## Permission Model en Brain OS

| Operación | Nivel | Razón |
|-----------|-------|-------|
| Leer archivos locales | AUTO | Sin riesgo |
| Consultar Notion (lectura) | AUTO | Sin riesgo |
| Escribir en `sesiones/` | AUTO | Solo logs |
| Mover archivos a `carrera/` | ASK_ONCE | Reorganiza filesystem |
| Sincronizar Aula Virtual | ASK_EACH | Conexión externa |
| Borrar archivos (cleanup) | ASK_EACH | Destructivo |

## Context Injection

El agente Brain OS usa los siguientes archivos como contexto base:
- `@brain_config.md` → IDs y esquemas
- `@INICIO.md` → estado del día
- `@skills/README.md` → catálogo de capacidades
