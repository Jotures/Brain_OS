# 🧠 Agent Memory Systems — Contexto Brain OS

## Mapeo de Tipos de Memoria en Brain OS

| Tipo de Memoria | Ubicación en Brain OS | Ejemplo |
|-----------------|----------------------|---------|
| **Episódica** | `sesiones/` | Logs de Pomodoro, qué estudiaste cada día |
| **Semántica** | `brain_config.md` | IDs de Notion, esquemas de BD, mapeo de cursos |
| **Procedimental** | `skills/` | Cómo ejecutar boot diario, cómo crear tareas |
| **De Trabajo** | Contexto activo de conversación | El prompt actual + archivos cargados |

## Estrategia de Recuperación

1. **Siempre cargar primero**: `brain_config.md` (fuente de verdad de IDs)
2. **Bajo demanda**: Contenido de cursos, historial de sesiones
3. **Nunca duplicar**: Si un dato vive en Notion, no replicarlo localmente

## Integración con Skills Existentes

- `system-coordinator` → verifica integridad de la memoria semántica
- `dashboard-sync` → refleja el estado de la memoria episódica en `INICIO.md`
- `pomodoro` → genera nuevos registros episódicos cada sesión

## Anti-Patrón a Evitar

❌ **Cargar todo siempre**: No inyectar toda la `brain_config.md` + todos los logs de sesiones en cada conversación. Usar la estrategia tiered del `context-window-management`.
