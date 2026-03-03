# 🧵 Conversation Memory — Contexto Brain OS

## Implementación del Hemingway Bridge

El Hemingway Bridge es el mecanismo de memoria de sesión entre sesiones de estudio. Se escribe al **final de cada sesión Pomodoro** y se lee al **inicio del siguiente boot**.

### Formato estándar del Hemingway Bridge

Guardar en `sesiones/YYYY-MM-DD-[materia]-sesion.md`:

```markdown
## 🧵 Hemingway Bridge — [Fecha] | [Materia]

**Estado al cierre:**
[Qué se logró en esta sesión en 1-2 líneas]

**Próximo paso exacto:**
[La acción ESPECÍFICA con la que retomar — no "continuar estudiando", sino "leer sección 3.2 sobre demanda agregada"]

**Contexto crítico (no olvidar):**
- [Dato o concepto que quedó pendiente de resolver]
- [Duda que necesita respuesta]

**Pendientes:**
- [ ] [Tarea concreta 1]
- [ ] [Tarea concreta 2]

**Nivel de energía al cierre:** [1-5] | **Modo sugerido para retomar:** TEACH / BRAINSTORM / IMPLEMENT
```

## Tipos de Memoria en Brain OS

| Tipo | Mecanismo | Cuándo activar |
|------|-----------|----------------|
| **Short-term** | Contexto de la conversación actual | Siempre activo |
| **Long-term** | `sesiones/` — Hemingway Bridge | Al iniciar boot diario |
| **Entity** | `brain_config.md` — IDs, materias, profesores | Siempre cargado |
| **Episódica** | Logs de Pomodoro en `tools/pomodoro/history.json` | Sous demanda |

## Protocolo de Lectura (Boot Diario)

Durante el Paso 5 del boot ("Hemingway Bridge"):
1. Leer el último archivo en `sesiones/` por materia prioritaria del día
2. Extraer el "Próximo paso exacto"
3. Incluirlo en el diagnóstico del día como primera acción recomendada

## Complementa

- `agent-memory-systems` (ya instalada) — arquitectura general
- `dashboard-sync` — refleja el estado del Hemingway en `INICIO.md`
- `autonomous-agent-patterns` — el Think del agent loop usa la memoria episódica
