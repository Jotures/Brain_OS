# 📋 CHANGELOG — Brain OS

Registro de cambios significativos del sistema. Formato: [fecha] [tipo] descripción.

**Tipos**: `feat` (nueva funcionalidad) · `refactor` (mejora interna) · `fix` (corrección) · `docs` (documentación) · `cleanup` (limpieza)

---

## 2026-03-03

- `feat` — Sprint 3: Creada skill `brain-os-health` con script `health_check.py` (auditoría automática, score 0-100)
- `docs` — `brain_config.md`: IDs de prioridad documentados como formato nativo de Notion
- `docs` — `last30days/` confirmada como skill legítima de investigación web (no requiere limpieza)
- `feat` — Sprint 2: Auto-documentación — `dashboard-sync` actualizado con sección de desarrollo, `dev_registry.json` creado, workflows mejorados con auto-update
- `feat` — Creado `config/dev_registry.json` (registro estructurado de cambios)
- `refactor` — `brain-os-dev.md` y `brain-os-upgrade.md` ahora incluyen paso de auto-documentación (CHANGELOG + dev_registry)
- `docs` — `dashboard-sync/references/sections.md` actualizado con plantilla de Estado de Desarrollo
- `cleanup` — Movidos 6 scripts sueltos (`_*.py`) de la raíz a `tools/scripts/`
- `feat` — Creado `CHANGELOG.md` para tracking de evolución del sistema
- `feat` — Creados 3 workflows de desarrollo: `/brain-os-dev`, `/brain-os-upgrade`, `/brain-os-audit`
- `docs` — Actualizado `INICIO.md` con sección de desarrollo del sistema

## 2026-02-12

- `feat` — Flujo Maestro actualizado a v2.0 (BRAC 90/20, Active Recall, Hemingway Bridge)
- `feat` — Integración Deep Research

## 2026-02-05

- `feat` — Integración Aula Virtual UAndina (Moodle)
- `feat` — Mapeo de cursos Moodle → Notion en `brain_config.md`

## 2026-02-04

- `feat` — Creación de 6 cursos universitarios + 1 personal en Notion
- `feat` — Configuración de 7 Notebooks en NotebookLM
- `feat` — Brain OS 2.0 — Setup inicial del semestre 2026-1
