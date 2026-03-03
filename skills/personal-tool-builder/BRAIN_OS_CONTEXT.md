# 🛠️ Personal Tool Builder — Contexto Brain OS

## Herramientas Construidas en Brain OS

| Herramienta | Ubicación | Stack | Estado |
|-------------|-----------|-------|--------|
| 🍅 Pomodoro Timer | `tools/pomodoro/` | Python + JSON config | ✅ Activo |
| 🧹 Cleanup Manager | `skills/cleanup-manager/` | Python scripts | ✅ Activo |
| 📥 Aula Virtual Sync | `skills/aula-virtual/scripts/` | Python + Playwright | ✅ Activo |
| 📊 Dashboard Sync | `skills/dashboard-sync/` | Markdown generation | ✅ Activo |

## Estándar de Herramientas Brain OS

Toda herramienta nueva debe seguir este patrón:

```
tools/[nombre]/
├── [nombre].py          # Script principal (Click CLI)
├── config.json          # Configuración (no hardcodear)
├── state.json           # Estado actual (persistente)
└── history.json         # Logs históricos
```

### Principios
1. **CLI con Click**: `@click.command()` para cada acción
2. **Config en JSON**: Nunca hardcodear paths ni IDs
3. **Logs en `sesiones/`**: Cada ejecución deja registro
4. **Notion sync opcional**: Si tiene métricas, sincronizar con BD_TRACKER_DIARIO

## Caso de Estudio: Pomodoro Timer

El Pomodoro es el ejemplo canónico de `personal-tool-builder` aplicado a Brain OS:
- **Itch**: "Necesito un timer que adapte la duración al tipo de materia"
- **Solución**: 5 perfiles + adaptive_rules en `brain_config.md`
- **Evolución**: Script simple → Active Recall integrado → Notion sync
