# 🔌 MCP Builder — Contexto Brain OS

## MCPs Activos en Brain OS

| MCP | Función | Estado |
|-----|---------|--------|
| `notion-mcp-server` | CRUD en BD_TAREAS, BD_AREAS, BD_RECURSOS | ✅ Activo |
| `supabase-mcp-server` | Base de datos Supabase | ✅ Disponible |

## MCPs Candidatos a Construir

### 1. `brain-os-mcp` (Prioridad Alta)
Un MCP dedicado que encapsule las operaciones frecuentes de Brain OS:
- `get_pending_tasks(curso?)` → consulta filtrada a Notion
- `start_pomodoro(topic, mode?)` → inicia Pomodoro con perfil auto-detectado
- `sync_aula_virtual()` → ejecuta descarga de Moodle
- `get_daily_diagnosis()` → recopila estado para el boot

### 2. `moodle-mcp` (Prioridad Media)
Wrapper sobre la API de Moodle/Aula Virtual:
- Listar cursos y tareas
- Descargar archivos nuevos
- Consultar notas y calificaciones

## Patrón de Implementación para Brain OS

Seguir la guía del `SKILL.md` con estas preferencias:
- **Lenguaje**: Python (alineado con los scripts existentes en `skills/aula-virtual/scripts/`)
- **Transporte**: stdio (ejecución local, no remota)
- **Autenticación**: Variables de entorno (`MOODLE_TOKEN`, `NOTION_TOKEN`)
- **Naming**: Prefijo `brain_os_` para todas las herramientas del MCP
