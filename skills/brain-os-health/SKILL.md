---
name: brain-os-health
description: Ejecuta una auditoría automática de salud de Brain OS. Verifica integridad de archivos core, skills, configuración, workflows y dashboard. Genera un reporte con score 0-100 y acciones recomendadas. Complementa el workflow /brain-os-audit.
---

# 🔍 Brain OS Health — Auditoría Automática

> Ejecuta un diagnóstico completo del sistema y genera un reporte con score de salud.

## Cuándo Usar

- Periódicamente cada 2-4 semanas
- Después de cambios grandes al sistema
- Cuando algo "se siente raro"
- El usuario dice "audita Brain OS", "health check", o `/brain-os-audit`

---

## Modo de Operación

Esta skill tiene dos modos:

### Modo 1: Script Automático (Recomendado)
```powershell
python skills/brain-os-health/scripts/health_check.py
```
Ejecuta todas las verificaciones y genera el reporte automáticamente.

### Modo 2: Manual (Paso a Paso)
Seguir el checklist del workflow `/brain-os-audit` manualmente.

---

## Verificaciones del Script

| # | Check | Peso | Qué verifica |
|---|-------|------|-------------|
| 1 | Archivos Core | 20% | `brain_config.md`, `INICIO.md`, `Flujo_Maestro_v2.md`, `CHANGELOG.md` existen y son legibles |
| 2 | Skills Health | 20% | Skills con `SKILL.md`, sin directorios vacíos |
| 3 | Config Válida | 15% | `brain_config.md` parseable, IDs presentes |
| 4 | Workflows | 15% | Todos en `.agent/workflows/` tienen frontmatter YAML |
| 5 | Dashboard | 15% | `INICIO.md` tiene sync reciente (< 7 días) |
| 6 | Git Status | 15% | Sin cambios sin commitear |

---

## Formato del Reporte

```
🔍 AUDITORÍA BRAIN OS — [Fecha]

📊 Score General: [X]/100

✅ Saludable:
   - [componente]: OK

⚠️ Atención:
   - [componente]: [problema menor]

🔴 Crítico:
   - [componente]: [problema bloqueante]

📋 Acciones Recomendadas:
   1. [acción prioritaria]
   2. [acción secundaria]
```

---

## Archivos de la Skill

```
skills/brain-os-health/
├── SKILL.md                  ← Este archivo
└── scripts/
    └── health_check.py       ← Script de auditoría automática
```

---

## Integración

- Complementa `/brain-os-audit` (workflow) con ejecución automatizada
- Resultados se registran en `config/audit_log.json`
- Puede ser invocada desde el boot diario (`Buenos días`) si score < 70
