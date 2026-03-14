---
name: context-window-management
description: "Gestión activa del contexto del agente: presupuesto de tokens, ciclo ZBrain de Context Engineering, evicción MaRS y estrategias anti-Context-Rot. Usar cuando: context window, token limit, context management, context engineering, long context, context rot."
source: Brain OS (basado en ZBrain, MaRS, AgeMem — research-agents-memory-2026)
trigger_conditions:
  - "Se está acabando el contexto"
  - "Context rot detectado"
  - "Optimizar uso de tokens"
  - "Estrategia de context engineering para [X]"
  - "El agente está olvidando instrucciones"
usage_constraints: "Solo para gestión técnica del context window del agente. No usar para gestión de memoria persistente (usar agent-memory-systems) ni para limpieza de archivos (usar cleanup-manager)."
category: "Sistema"
parameters:
  strategy: "Estrategia: budget | eviction | clearing | compression"
---

# Context Window Management

> Eres un especialista en context engineering que ha optimizado aplicaciones LLM en millones de conversaciones. Sabes que **el contexto es un recurso finito con rendimientos decrecientes**. Más tokens ≠ mejores resultados. El arte está en curar la información correcta.

---

## 🔑 Principios Fundamentales (Basados en Investigación Académica)

1. **"Un contexto largo no es memoria"** — AgeMem (2024). Ventanas masivas activan el síndrome *lost-in-the-middle*: el LLM ignora información en el centro del prompt.
2. **Context Rot es silencioso** — La degradación de calidad no se anuncia; el agente simplemente da respuestas peores sin ser consciente.
3. **El olvido deliberado es una feature, no un bug** — Reiniciar el contexto selectivamente mejora el foco y previene loops de razonamiento.
4. **Presupuesto activo**: Ver `MEMORY_GOVERNANCE.token_budget` en `brain_config.md` (default: 6,000 tokens).

---

## 🔄 Ciclo ZBrain — Context Engineering Iterativo

> **Fuente**: ZBrain Enterprise Agents (2025). Aplicar en cada turno o bloque de trabajo.

```
Pensamiento → Acción → Observación → Memory Refresh → Siguiente pensamiento
```

| Fase | Qué hacer |
|---|---|
| **Pensamiento** | Analizar el estado actual del contexto. ¿Qué información es activa y relevante? |
| **Acción** | Ejecutar la herramienta o responder con información curada |
| **Observación** | Evaluar el resultado. ¿Se logró el objetivo parcial? |
| **Memory Refresh** | Actualizar el "estado activo": descartar lo resuelto, retener lo pendiente |
| **Siguiente** | Proceder con contexto optimizado |

---

## 📊 Estrategia por Tamaño de Contexto

| Tamaño | Señal | Estrategia |
|:---:|---|---|
| < 3k tokens | Normal | Ninguna acción especial |
| 3k-6k tokens | Monitoreo | Activar Progressive Disclosure agresivo |
| > 6k tokens | Context Rot Risk | Activar Protocolo MaRS (ver agent-memory-systems) |
| > 10k tokens | Saturación | Context Clearing deliberado + mini Hemingway Bridge |

---

## 🧠 Estrategias Operativas

### 1. Serial Position Optimization
Colocar la información más importante al **inicio** y al **final** del prompt. El LLM tiene mejor recall de los extremos que del centro.
```
[Instrucciones críticas] → [Información de trabajo] → [Recordatorios clave]
```

### 2. Intelligent Summarization (por importancia, no por recencia)
NO comprimir solo porque algo es "viejo". Comprimir basado en relevancia para el objetivo activo.
```
Alta relevancia → Preservar íntegro
Media relevancia → Comprimir a 1-2 líneas clave
Baja relevancia → Descartar
Dominio cerrado → Descartar completo (Higiene MaRS Fase 1)
```

### 3. Context Routing (Tiered Strategy)
- **Tier 1 (Hot)**: STM activa — información del turno actual
- **Tier 2 (Warm)**: Episodic reciente — últimos 5 episodios del hilo
- **Tier 3 (Cold)**: Semantic LTM — `config/semantic_memory.json` (gists abstractos)

Cuando Tier 1 se satura, mover información relevante a Tier 2 o 3 antes de descartar.

---

## ⚠️ Anti-Patrones a Evitar

| Anti-Patrón | Riesgo | Solución |
|---|---|---|
| **Naive Truncation** | Cortar información al azar destruye coherencia | Evicción por prioridad (MaRS Fase 3) |
| **One-Size-Fits-All** | Tratar todo el contexto igual | Tiered strategy según dominio |
| **Ignoring Token Costs** | Acumular sin límite → Context Rot | Monitorear contra `token_budget` |
| **Summarization Drift** | Comprimir pierde detalles críticos | Preservar hechos concretos; comprimir narrativa |

---

## Related Skills
- `agent-memory-systems`: Patrones MaRS, AgeMem (Context Clearing), FER (REM)
- `autonomous-agent-patterns`: Detección de loops, selección de patrón por complejidad
- `conversation-memory`: Gestión de memoria episódica entre conversaciones
