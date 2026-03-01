# 🗺️ Mapeo: Conceptos Deep Research → Skills de Brain OS

> **Objetivo**: Identificar qué hallazgos de la investigación ya están cubiertos por skills existentes, cuáles necesitan mejoras, y cuáles requieren skills nuevas.

---

## Skills Existentes y Su Cobertura

### 🍅 `pomodoro` — Timer Adaptativo

| Concepto de Deep Research | Estado | Acción |
|--------------------------|--------|--------|
| Timer adaptativo por carga cognitiva (15/25/50 min) | ✅ Cubierto | Ya soporta `default`, `intensive` |
| Ciclos ultradianos BRAC 90/20 | ❌ No cubierto | Agregar modo `ultradian` |
| Cronotipos (Lion/Bear/Wolf/Dolphin) | ❌ No cubierto | Usar para sugerir duración óptima |
| Active Recall post-Pomodoro | ❌ No cubierto | Integrar prompts de autotest al break |
| Interleaving entre Pomodoros | 🔶 Parcial | Sugerir cambio de tema entre sesiones |

---

### 🔗 `system-coordinator` — Verificación del Sistema

| Concepto de Deep Research | Estado | Acción |
|--------------------------|--------|--------|
| DAG curricular (prerequisitos) | ❌ No cubierto | Agregar lógica de dependencias entre cursos |
| Betweenness centrality | ❌ No cubierto | Calcular cursos "cuello de botella" |
| SAP 67%/150% tracking | ❌ No cubierto | Monitorear progreso académico |
| Critical Path Method | ❌ No cubierto | Identificar secuencia inamovible |
| PARA clasificación de archivos | 🔶 Parcial | La estructura `carrera/` ya usa categorías |

---

### 🔄 `dashboard-sync` — Panel de Control

| Concepto de Deep Research | Estado | Acción |
|--------------------------|--------|--------|
| Hemingway Bridge (hilo del día anterior) | ❌ No cubierto | Mostrar en dashboard matutino |
| XP / Gamificación visual | ❌ No cubierto | Barra de progreso + nivel |
| Streak con loss aversion | ✅ Cubierto | Ya existe sistema de rachas |
| Goal-Gradient Effect | ❌ No cubierto | Mostrar % hacia hito semanal |
| Distribución óptima por cronotipo | ❌ No cubierto | Personalizar sugerencias por hora |

---

### 🎓 `aula-virtual` — Conexión Moodle

| Concepto de Deep Research | Estado | Acción |
|--------------------------|--------|--------|
| Sync bidireccional Notion↔Moodle | ✅ Cubierto | Ya sincroniza tareas/archivos |
| Idempotencia (evitar duplicados) | ✅ Cubierto | Usa `pending_notion_sync.json` |
| Timezone handling | ⚠️ Verificar | Confirmar manejo de UTC vs local |
| Captura automática de clases | ❌ No cubierto | Requiere hardware (Plaud Note) |

---

### 📚 `notebooklm` — Cerebro Secundario

| Concepto de Deep Research | Estado | Acción |
|--------------------------|--------|--------|
| RAG source-grounded | ✅ Cubierto | Ya funciona via browser automation |
| Audio Overview como warm-up | 🔶 Parcial | Existe pero no integrado al flujo |
| Deep Research agent | ❌ No cubierto | Explorar nuevas funcionalidades |
| Progressive Summarization | ❌ No cubierto | Auto-generar Capa 1 al ingestar |
| Prompt templates académicos | ❌ No cubierto | Inyectar prompts del Bloque 3 |

---

### 📂 `library-manager` — Bibliotecario

| Concepto de Deep Research | Estado | Acción |
|--------------------------|--------|--------|
| Organización PARA | 🔶 Parcial | Clasifica por curso, no por P/A/R/A |
| Resumen automático al registrar | ❌ No cubierto | Progressive Summarization Capa 1 |
| Metadata enrichment | ❌ No cubierto | Tipo, autor, temas clave |
| Zettelkasten linking | ❌ No cubierto | Requiere Obsidian, fuera de scope |

---

## Skills Sin Mapeo Directo (Necesitan Skills Nuevas)

| Concepto | Skill Propuesta | Complejidad |
|----------|----------------|-------------|
| Preparación de debates (Toulmin Model) | `debate-prep` | Baja |
| Preparación de exposiciones (ABT + Mayer) | `presentation-prep` | Baja |
| Técnica Feynman guiada por IA | `feynman-practice` | Baja |
| Planificación multi-semestre (DAG + CPM) | `semester-planner` | Alta |
| Gestión de energía por cronotipo | `energy-tracker` | Media |
| Generación de flashcards Anki | `flashcard-gen` | Media |

---

## Matriz de Cobertura Visual

```
Concepto              | pomodoro | coordinator | dashboard | aula | notebook | library
──────────────────────|──────────|─────────────|───────────|──────|──────────|────────
Active Recall         |    🔶    |             |           |      |          |
Pomodoro Adaptativo   |    ✅    |             |           |      |          |
Feynman               |          |             |           |      |    🔶    |
Spacing/Anki          |    🔶    |             |           |      |          |
Gamificación/XP       |          |             |    🔶     |      |          |
Cronotipos/Energía    |    ❌    |             |    ❌     |      |          |
MCP Integration       |          |      ✅     |           |  ✅  |    ✅    |
Hemingway Bridge      |          |             |    ❌     |      |          |
PARA Method           |          |      🔶     |           |      |          |   🔶
Progressive Summary   |          |             |           |      |    ❌    |   ❌
DAG Curricular        |          |      ❌     |           |      |          |
Prompts Académicos    |          |             |           |      |    ❌    |

✅ = Cubierto    🔶 = Parcial    ❌ = No cubierto (oportunidad)
```

---

## Top 5 Conceptos con Mayor ROI si se Integran

1. **Active Recall Post-Pomodoro** → `pomodoro` skill → Bajo esfuerzo, alto impacto pedagógico
2. **Hemingway Bridge** → `dashboard-sync` → Bajo esfuerzo, reduce fricción de reenganche
3. **BRAC 90/20** → `pomodoro` → Medio esfuerzo, alinea con fisiología
4. **Progressive Summarization** → `library-manager` + `notebooklm` → Medio esfuerzo, enriquece todo recurso
5. **Macro "Buenos días"** → workflow → Bajo esfuerzo, elimina decision fatigue
