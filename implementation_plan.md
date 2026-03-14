# Plan Maestro: Brain OS 2.2 — Mejoras de Arquitectura Cognitiva

Upgrading Brain OS del estado actual (2.1) a una arquitectura 2.2 basada en los hallazgos del ciclo de investigación con NotebookLM. Las mejoras están organizadas en 3 fases por impacto vs. complejidad.

> [!IMPORTANT]
> Los cambios de **Fase 1** son quirúrgicos (ediciones a archivos existentes). Los de **Fase 2** crean contenido nuevo. La **Fase 3** requiere un script Python nuevo.

---

## FASE 1 — Quick Wins (Baja Complejidad, Alto Impacto)
*Objetivo: Fortalecer el sistema de memoria y los ciclos FER con cambios mínimos.*

### [Memoria Semántica]

#### [MODIFY] [semantic_memory.json](file:///c:/Users/Ruben%20J/Documents/Antigravito%20Proyects/Brain_OS/config/semantic_memory.json)
- Añadir campo `"score": 1-10` a cada entrada (actualmente solo existe `"confidence": "high|medium|low"`).
- Establecer la regla de ingesta: **score < 4 → no se persiste al semantic_memory**; queda solo en el log de sesión.
- Añadir campo `"eviction_candidate": true|false` derivado del score y la recencia.

---

### [Esquema de Sesiones]

#### [MODIFY] Esquema de logs en `sesiones/`
- Agregar campo `"fer_processed": false` al template de cada log diario.
- El ciclo FER lo marcará como `true` al consolidar el gist, permitiendo que `cleanup-manager` la identifique y limpie sin riesgo.
- Este campo es el **puente inteligente** entre la memoria episódica y la semántica.

---

### [Elite Skill Architect]

#### [MODIFY] [SKILL.md](file:///c:/Users/Ruben%20J/Documents/Antigravito%20Proyects/Brain_OS/skills/elite-skill-architect/SKILL.md)
- Agregar al **Modo 3 (Rehacer)**: límite explícito de **máx. 5 iteraciones** del bucle Crítica → Refinamiento.
- En la iteración 5: el agente detiene el bucle, presenta la mejor versión alcanzada y el feedback no resuelto, y solicita aprobación humana.
- Añadir nueva sección `## Política de Escalamiento` que documente este mecanismo.

---

### [Cleanup Manager]

#### [MODIFY] [SKILL.md](file:///c:/Users/Ruben%20J/Documents/Antigravito%20Proyects/Brain_OS/skills/cleanup-manager/SKILL.md)
- Agregar **Categoría 9: Logs de sesión ya procesados por FER**.
- Regla: si un log en `sesiones/` tiene `"fer_processed": true` Y tiene más de **7 días** de antigüedad → candidato a `Limpieza conservadora` (Nivel 2).
- Esto implementa el mecanismo de **TTL (Time-to-Live)** con validación semántica.

---

## FASE 2 — Arquitectura Nueva (Complejidad Media)
*Objetivo: Hacer que el agente tome decisiones autónomas y de alta calidad.*

### [Skills — Frontmatter YAML]

#### [MODIFY] Frontmatter de las **29 skills** en `skills/*/SKILL.md`
Añadir a cada skill los siguientes campos para habilitar la **autoselección semántica**:

```yaml
trigger_conditions:
  - "caso de uso 1 que dispara esta skill"
  - "caso de uso 2"
usage_constraints: "Para qué NO usar esta skill (ej. no usar para código, solo para texto)"
category: "Investigación | Escritura | Planificación | Académico | Sistema | Documentos"
parameters:
  param1: "descripción y tipo"
```

> [!IMPORTANT]
> Priorizar primero las 8 skills de uso frecuente: `research-engineer`, `planning`, `notebooklm`, `system-coordinator`, `elite-skill-architect`, `agent-memory-systems`, `cleanup-manager`, `aula-virtual`.

---

### [Nueva Skill: Study Router]

#### [NEW] `skills/study-router/SKILL.md`
Codifica el **árbol de decisión** para el comando `¿Qué debo estudiar?`:
- **Rama Notion** (memoria estructurada): fechas, urgencia, estado de tareas → QUÉ y CUÁNDO.
- **Rama NotebookLM** (RAG semántico): extracción de conceptos, preguntas de examen → CÓMO.
- **Rama Híbrida**: Notion define el tema → NotebookLM entrega el contenido.

Esta skill reemplaza la lógica implícita y dispersa actualmente en `system-coordinator`.

---

### [Modo Crisis — Patrón Secuencial]

#### [MODIFY] Skill o workflow de `Modo Crisis`
- Formalizar el **patrón secuencial**: Agente Síntesis → Agente Evaluador.
- Paso 1: `research-engineer` procesa `03_Notas/` y PDFs → entrega resumen estructurado.
- Paso 2: Agente evaluador recibe **solo ese resumen** para generar el examen de prueba.
- Documentar en el workflow `/brain-os-study` o en el `system-coordinator`.

---

## FASE 3 — Analítica Avanzada (Complejidad Alta)
*Objetivo: Detección temprana de riesgo académico basada en datos reales.*

### [Script de Score de Riesgo]

#### [NEW] `skills/pomodoro/scripts/risk_score.py`
Script Python que lee los logs de `sesiones/` y calcula semanalmente los **5 indicadores de alerta temprana**:

| Indicador | Fórmula | Umbral de Alerta |
|---|---|---|
| Tasa de abandono | Pomodoros abortados / iniciados | > 20% → 🔴 |
| Velocidad de consolidación | Gists score>7 / Pomodoro completado | < 0.5 → 🟡 |
| Ratio Modo Crisis | Pomodoros en crisis / total | > 60% → 🔴 |
| Execution Gap | Planificados - Ejecutados | > 3 → 🟡 |
| Recovery Decay | Tiempo de descanso promedio | > 15 min → 🟡 |

Output: un bloque de estado que el comando `"Resume semana"` lee e integra en su reporte.

---

## Verification Plan

### Fase 1
- Ciclo FER: verificar que los nuevos gists en [semantic_memory.json](file:///c:/Users/Ruben%20J/Documents/Antigravito%20Proyects/Brain_OS/config/semantic_memory.json) contienen el campo `score`.
- Ciclo Cleanup: ejecutar `"Escanear basura"` y confirmar que aparece la nueva **Categoría 9**.
- Elite Skill Architect: ejecutar un `"Rehace la skill [nombre]"` y verificar que el bucle se detiene en iteración 5.

### Fase 2
- Ejecutar `"¿Qué debo estudiar?"` y verificar que el agente sigue el árbol de decisión Notion → NotebookLM.
- Ejecutar `"Modo Crisis Economía Internacional"` y verificar el flujo secuencial de dos agentes.

### Fase 3
- Ejecutar `risk_score.py` contra logs de `sesiones/` y comparar output vs. expectativa manual.
- Ejecutar `"Resume semana"` y verificar que el Score de Riesgo aparece en el reporte final.
