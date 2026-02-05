---
name: dashboard-sync
description: Sincroniza automáticamente el archivo INICIO.md (panel de control de Brain OS) con la información actual del sistema. Usa esta skill cuando: (1) Se agreguen nuevos notebooks a NotebookLM, (2) Se implementen nuevas funcionalidades, (3) Se quiera actualizar el dashboard manualmente, (4) Se diga "Actualiza el dashboard", "Sincroniza INICIO.md", o "Actualiza el panel de control".
---

# Dashboard Sync

Sincroniza automáticamente `INICIO.md` con la información actual de Brain OS.

## Cuándo Usar

- Después de agregar notebooks a NotebookLM
- Después de implementar nuevas integraciones (Notion, Aula Virtual, etc.)
- Cuando el usuario pida "Actualiza el dashboard" o similar
- Al inicio de cada semestre o aporte

## Flujo de Sincronización

```
1. Leer brain_config.md → Obtener cursos y notebooks
2. Escanear skills/ → Contar y categorizar skills
3. Consultar tareas en Notion (opcional) → Tareas pendientes
4. Actualizar INICIO.md → Secciones específicas
```

## Secciones a Actualizar

| Sección | Fuente | Descripción |
|---------|--------|-------------|
| 🔬 Avanzados | `brain_config.md` | Comandos NotebookLM por curso |
| 🛠️ Skills | `skills/` directory | Conteo y categorías |
| 📊 Estado Actual | Sistema | Semestre, aporte, métricas |
| 📅 Próximas Tareas | Notion BD_TAREAS | Tareas pendientes |

## Uso

### Automático (Post-implementación)

Después de cualquier implementación que afecte el dashboard:

```bash
# Ejecutar sincronización
python scripts/sync_dashboard.py

# Preview sin modificar
python scripts/sync_dashboard.py --preview
```

### Manual

El agente debe:
1. Leer `brain_config.md` para obtener la configuración actual
2. Identificar qué secciones de `INICIO.md` necesitan actualización
3. Aplicar los cambios usando las plantillas de `references/sections.md`

## Plantillas de Secciones

### Comandos NotebookLM

```markdown
### 🔬 NotebookLM (Conectado ✅)

| Curso | Comando |
|-------|---------|
| 📗 Economía Ambiental | "Consulta mi libro de Economía Ambiental" |
| 📘 Economía Internacional I | "Consulta mi libro de Economía Internacional" |
...
```

### Skills Disponibles

```markdown
## 🛠️ SKILLS DISPONIBLES ([COUNT])

| Categoría | Skills |
|-----------|--------|
| 📄 Docs | `docx` `xlsx`... |
| 🔍 Investigar | `notebooklm` `research-engineer` |
| 🔄 Sistema | `dashboard-sync` |
```

## Archivos de Referencia

- `references/sections.md` - Definición detallada de cada sección y su formato
- `scripts/sync_dashboard.py` - Script para sincronización automática (opcional)

## Notas

- Esta skill se ejecuta principalmente por el agente, no requiere scripts complejos
- El agente debe leer los archivos fuente y actualizar `INICIO.md` directamente
- Siempre hacer backup mental del estado anterior antes de modificar
