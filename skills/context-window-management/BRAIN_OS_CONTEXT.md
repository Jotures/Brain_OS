# 📦 Context Window Management — Contexto Brain OS

## Protocolo de Prioridad de Carga

### Tier 1 — Siempre (cada conversación)
- `brain_config.md` → secciones de IDs activas
- Estado actual del usuario (cronotipo/hora del día)
- Tareas urgentes (Notion: `Días Restantes < 3`)

### Tier 2 — Bajo demanda (cuando el usuario lo pide)
- Contenido específico de un curso (`carrera/semestres/2026-1/cursos/...`)
- Historial de sesiones Pomodoro (`sesiones/`)
- Skill SKILL.md específica

### Tier 3 — Nunca cargar completo
- Todos los logs de sesiones históricos → resumir
- Todas las skills → solo la relevante
- Brain_OS_Master_Doc completo → solo la sección necesaria

## Aplicación al Boot Diario ("Buenos días")

El boot diario es el flujo que más contexto consume. Optimización:

```
Paso 1 (system-coordinator): Solo verificar IDs → ~200 tokens
Paso 2 (aula-virtual sync): Solo cambios nuevos → variable
Paso 3 (dashboard-sync): Regenerar INICIO.md → ~300 tokens
Paso 4 (diagnóstico): Tareas Notion filtradas → ~500 tokens
Paso 5 (Hemingway Bridge): 1 línea de ayer → ~50 tokens
```

## Serial Position Effect

Colocar información crítica (deadlines, tareas urgentes) al **inicio y final** del contexto. La información intermedia (detalles de configuración) se pierde con más facilidad.
