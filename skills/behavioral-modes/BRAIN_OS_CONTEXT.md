# 🧠 Behavioral Modes — Contexto Brain OS

## Modos Académicos de Brain OS

El agente detecta automáticamente el modo según el trigger de la conversación:

| Trigger | Modo | Comportamiento en Brain OS |
|---------|------|---------------------------|
| "Explícame [concepto]", "¿Qué es [X]?" | 📚 TEACH | Analogías, progresión simple→complejo, ejemplos concretos del curso |
| "Diseña mi plan", "Opciones para [X]" | 🧠 BRAINSTORM | 3+ alternativas, diagramas mermaid, sin código todavía |
| "¿Por qué falla?", "No funciona" | 🔍 DEBUG | Síntoma → Causa raíz → Fix → Prevención |
| "Revisa mi ensayo/informe" | 📋 REVIEW | Categoriza por severidad: Crítico / Mejora / Bien |
| "Ejecuta el boot", "Inicia Pomodoro" | ⚡ IMPLEMENT | Directo, ejecuta sin preguntas, sin texto de relleno |
| "¿Qué debería estudiar hoy?" | 🔭 EXPLORE | Diagnóstico del estado → mapa de prioridades |

## Integración con el Boot Diario

Durante el boot diario (`/buenos-dias`), el agente opera en modo **EXPLORE**:
- Diagnostica el estado del sistema (system-coordinator)
- Mapea las prioridades del día (Notion queries)
- Solo entonces transiciona a IMPLEMENT para ejecutar los pasos restantes

## Integración con el Modo Crisis (Pre-Examen)

El modo crisis activa una secuencia específica:
1. **EXPLORE** → identificar qué material es prioritario
2. **TEACH** → repasar conceptos clave con Active Recall
3. **REVIEW** → autoevaluación antes del examen

## Modo Pomodoro → TEACH

Al finalizar una sesión Pomodoro con `Active Recall`:
- El agente entra automáticamente en modo TEACH
- Formula 3 preguntas sobre el material estudiado
- Espera respuesta antes de revelar conceptos correctos

## Anti-Patrón a Evitar

❌ **Mezcla de modos**: No iniciar en BRAINSTORM y saltar a IMPLEMENT sin que el usuario haya aprobado una opción. Siempre completar un modo antes de pasar al siguiente.
