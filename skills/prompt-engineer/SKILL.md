---
name: prompt-engineer
description: Experto en diseño y optimización de prompts para LLMs. Domina estructura de prompts, gestión de contexto, formato de outputs, few-shot, chain-of-thought y evaluación sistemática. Usar cuando el usuario diga "Diseña un prompt para [X]", "Mejora este prompt", "Prompt engineering", "System prompt", "Few-shot", "Chain of thought", o cuando necesite crear/mejorar prompts para skills o aplicaciones LLM.
source: vibeship-spawner-skills (Apache 2.0) — adaptado para Brain OS
trigger_conditions:
  - "Diseña un prompt para [X]"
  - "Mejora este prompt"
  - "Crea un system prompt para [agente]"
  - "Optimiza el prompt de [skill]"
  - "Evalúa este prompt sistemáticamente"
usage_constraints: "Para diseñar y optimizar prompts específicos. Para aprender patrones teóricos, usar prompt-engineering. Para buscar prompts existentes, usar prompt-library."
category: "Escritura"
parameters:
  task: "Tarea para la cual diseñar el prompt (string)"
  model: "Modelo objetivo: gpt-4 | claude | gemini | general (default: general)"
---

# 🧠 Prompt Engineer

> Traduce intención en instrucciones que los LLMs realmente siguen. Los prompts son programación — necesitan el mismo rigor que el código.

## Cuándo Usar

- Crear system prompts para nuevas skills de Brain OS
- Optimizar prompts existentes que no dan buenos resultados
- Diseñar few-shot examples para tareas repetitivas
- Evaluar por qué un prompt produce resultados inconsistentes
- Cuando el usuario dice "Diseña un prompt", "Mejora este prompt"

---

## Comandos

| Comando | Función |
|---------|---------|
| "Diseña un prompt para [X]" | Crea prompt estructurado desde cero |
| "Mejora este prompt: [texto]" | Analiza y optimiza un prompt existente |
| "Evalúa este prompt" | Score /10 con feedback específico |
| "Crea few-shot examples para [tarea]" | Genera 3-5 ejemplos diversos |
| "Chain of thought para [problema]" | Diseña CoT con pasos intermedios |

---

## Patrones de Diseño

### 1. System Prompt Estructurado

La anatomía de un system prompt efectivo:

```markdown
# Estructura Recomendada

1. ROLE       → Quién es el modelo (identidad concreta)
2. CONTEXT    → Background relevante (mínimo necesario)
3. TASK       → Qué debe hacer (instrucciones claras)
4. CONSTRAINTS→ Qué NO debe hacer (límites explícitos)
5. OUTPUT     → Formato esperado (estructura exacta)
6. EXAMPLES   → Demostración de comportamiento correcto
```

**Ejemplo aplicado a Brain OS:**
```
Role: Eres un tutor académico especializado en Economía.
Context: El usuario es un estudiante de 5to semestre de Economía en UAndina.
Task: Responde preguntas sobre el material del curso usando las fuentes proporcionadas.
Constraints: NO inventes datos. Si no sabes, di "No tengo esa información".
Output: Respuestas en español, máximo 3 párrafos, con citas a la fuente.
Examples:
  Pregunta: "¿Qué es la ventaja comparativa?"
  Respuesta: "Según Ricardo (Fuente: Cap. 3), la ventaja comparativa..."
```

### 2. Few-Shot Examples

Incluir ejemplos del comportamiento deseado:

```markdown
# Reglas para Few-Shot

- Mostrar 2-5 ejemplos diversos
- Incluir edge cases en los ejemplos
- Igualar la dificultad de los ejemplos al input esperado
- Formato consistente entre todos los ejemplos
- Incluir ejemplos negativos cuando ayude
```

**Ejemplo:**
```
## Buenos ejemplos:
Input: "¿Cuánto es 25% de 80?"
Output: "20. (80 × 0.25 = 20)"

## Ejemplo negativo (qué NO hacer):
Input: "¿Cuánto es 25% de 80?"
Output: "El porcentaje es un concepto matemático que..." ← demasiado largo
```

### 3. Chain-of-Thought (CoT)

Pedir razonamiento paso a paso:

```markdown
# Cuándo Usar CoT

✅ Problemas matemáticos o lógicos
✅ Decisiones con múltiples factores
✅ Debugging de errores complejos
✅ Análisis comparativo

❌ Tareas simples de lookup
❌ Preguntas con respuesta directa
❌ Generación creativa libre
```

**Template CoT:**
```
Analiza el siguiente problema paso a paso:
1. Identifica los datos disponibles
2. Determina qué se necesita resolver
3. Aplica el método apropiado
4. Verifica tu respuesta
5. Presenta el resultado final

Muestra tu razonamiento completo antes de dar la respuesta.
```

---

## Anti-Patterns

### ❌ Instrucciones Vagas

| Mal | Bien |
|-----|------|
| "Responde bien" | "Responde en máximo 3 oraciones, citando la fuente" |
| "Sé conciso" | "Máximo 50 palabras por respuesta" |
| "Sé útil" | "Proporciona 3 opciones con pros y contras" |

> **Por qué falla**: El modelo interpreta "bien" y "conciso" de formas impredecibles. La ambigüedad es el enemigo.

### ❌ Kitchen Sink Prompt (demasiado contexto)

| Mal | Bien |
|-----|------|
| 2000 palabras de instrucciones | 300-500 palabras enfocadas |
| "Aquí tienes todo el manual..." | "Estos son los 3 puntos clave..." |
| Contexto "por si acaso" | Solo contexto que afecta el output |

> **Por qué falla**: El modelo pierde foco con demasiado contexto. Lo importante se diluye en lo accesorio.

### ❌ Sin Instrucciones Negativas

| Mal | Bien |
|-----|------|
| "Resume el texto" | "Resume el texto. NO incluyas opiniones personales. NO excedas 100 palabras." |
| "Genera código" | "Genera código. NO uses librerías externas. NO incluyas comentarios triviales." |

> **Por qué falla**: Los modelos necesitan saber qué evitar tanto como qué hacer. Sin límites, generan contenido inesperado.

---

## ⚠️ Sharp Edges

| Issue | Severidad | Solución |
|-------|:---------:|----------|
| Lenguaje impreciso | 🔴 Alta | Usar verbos de acción específicos: "Lista 5...", "Compara X vs Y" |
| Esperar formato sin especificarlo | 🔴 Alta | Incluir template exacto del output esperado |
| Solo decir qué hacer, no qué evitar | 🟡 Media | Agregar sección "Constraints" con 3-5 prohibiciones |
| Cambiar prompts sin medir impacto | 🟡 Media | Evaluar antes/después con 5 inputs de prueba idénticos |
| Contexto irrelevante "por si acaso" | 🟡 Media | Preguntarse: "¿Cambiaría el output sin este contexto?" |
| Ejemplos sesgados o no representativos | 🟡 Media | Incluir variedad: simple, complejo, edge case, negativo |
| Temperatura default para todas las tareas | 🟡 Media | Factual: 0-0.3 / Creativo: 0.7-1.0 / Code: 0 |
| No considerar prompt injection | 🔴 Alta | Delimitar input del usuario con tags: `<user_input>...</user_input>` |

---

## Integración con Brain OS

Esta skill es especialmente útil para:

| Caso | Cómo ayuda |
|------|-----------|
| Crear skills | Diseñar la `description` del frontmatter (trigger de activación) |
| Mejorar `elite-skill-architect` | Optimizar templates de generación de prompts |
| Pomodoro Active Recall | Diseñar prompts para preguntas de Bloom nivel 3-4 |
| NotebookLM queries | Formular preguntas que maximicen grounded answers |

---

## 🧪 Escenarios de Prueba

### Test 1: Diseño desde cero

```
Input:    "Diseña un prompt para un chatbot de soporte técnico"
Espera:   Prompt con las 6 secciones (Role→Examples)
Verifica: - Tiene Role, Context, Task, Constraints, Output, Examples
          - Constraints incluye ≥3 prohibiciones
Output:   Prompt completo + explicación de cada decisión
```

### Test 2: Mejora de prompt existente

```
Input:    "Mejora este prompt: 'Responde preguntas sobre economía'"
Espera:   Análisis de debilidades + versión mejorada
Verifica: - Identifica al menos 2 problemas
          - Versión mejorada es ≥3x más específica
Output:   Score antes/después + diff de cambios
```

### Test 3: Evaluación

```
Input:    "Evalúa este prompt: [prompt de 50 palabras]"
Espera:   Score /10 con feedback en 5 dimensiones
Verifica: Cubre: claridad, especificidad, constraints, formato, examples
Output:   Tabla con scores parciales + recomendaciones
```

---

## Skills Relacionadas

| Complemento | Para qué |
|------------|----------|
| `elite-skill-architect` | Crear skills completas (este ayuda con la parte del prompt) |
| `prompt-engineering` | Técnicas más avanzadas de prompt design |
| `prompt-library` | Biblioteca de prompts reutilizables |
| `research-engineer` | Context research antes de diseñar prompts |
