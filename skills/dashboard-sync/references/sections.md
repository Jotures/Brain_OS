# Secciones de INICIO.md

Definición de las secciones del dashboard y su formato para sincronización.

## Mapeo de Fuentes

| Sección | Fuente | Ruta |
|---------|--------|------|
| NotebookLM | Library JSON | `skills/notebooklm/data/library.json` |
| Skills | Directorio | `skills/*/SKILL.md` |
| Estado | Config | `brain_config.md` |
| Tareas | Notion | `BD_TAREAS_MAESTRAS` |
| Cursos | Config | `brain_config.md` → Cursos del Semestre |

## Plantilla: NotebookLM

```markdown
### 🔬 NotebookLM (Conectado ✅)

| Curso | Comando |
|-------|---------|
| 📗 {curso_name} | "Consulta mi libro de {curso_name}" |
```

## Plantilla: Skills

```markdown
## 🛠️ SKILLS DISPONIBLES ({count})

| Categoría | Skills |
|-----------|--------|
| 📄 Docs | `docx` `xlsx` `pptx` `pdf` |
| ✍️ Escribir | `copywriting` `copy-editing` `content-creator` |
| 📋 Planificar | `brainstorming` `writing-plans` `concise-planning` |
| 🔍 Investigar | `notebooklm` `research-engineer` |
| 🔄 Sistema | `dashboard-sync` `skill-creator` |

**Uso**: `"Usa la skill [nombre] para [tarea]"`
```

## Plantilla: Estado Actual

```markdown
## 📊 ESTADO ACTUAL

| Métrica | Valor |
|---------|-------|
| Semestre | {semestre} |
| Aporte | {aporte} (en curso) |
| Cursos activos | {num_cursos} |
| Tareas pendientes | {num_tareas} |
| Racha | {racha} días |
```

## Plantilla: Próximas Tareas

```markdown
## 📅 PRÓXIMAS TAREAS

| Tarea | Curso | Entrega | Prioridad |
|-------|-------|---------|-----------|
| {tarea_name} | {curso} | {fecha} | {emoji} |
```

## Emojis por Curso

| Curso | Emoji |
|-------|-------|
| Economía Ambiental | 📗 |
| Economía Internacional I | 📘 |
| Economía y Gestión Pública | 📙 |
| Investigación Operativa | 📕 |
| Teoría Monetaria y Bancaria | 📔 |
| Investigación Económica | 📓 |
| Inglés | 📒 |
