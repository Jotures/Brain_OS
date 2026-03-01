# 🧠 Prompt Templates para Active Recall Post-Pomodoro

> Basado en Deep Research: Prompting para Estudio, Técnica Feynman, Active Recall & Anki
> Uso: El agente Brain OS selecciona el template apropiado al finalizar cada sesión de Pomodoro

---

## Autotest — Bloom Nivel 3-4 (Aplicar/Analizar)

**Cuándo**: Después de cada sesión de estudio (default)

```
Genera 3 preguntas sobre [TEMA] del curso [CURSO]:
- 1 pregunta de APLICACIÓN: "¿Cómo usarías X para resolver Y?"
- 1 pregunta de ANÁLISIS: "¿Qué diferencia hay entre X e Y?" o "¿Por qué X causa Y?"
- 1 pregunta de CONEXIÓN: "¿Cómo se relaciona X con [concepto de otro curso]?"

Nivel: universitario de economía. No preguntas de memoria pura (fechas, definiciones textuales).
Formato: preguntas directas, sin opciones múltiples.
```

---

## Feynman Check — Verificar Comprensión Real

**Cuándo**: Si el usuario estudió un concepto abstracto o complejo

```
Actúa como un estudiante curioso de 15 años. Yo voy a explicarte [CONCEPTO].
Tu trabajo es:
1. Escuchar mi explicación
2. Señalar exactamente dónde mi explicación se vuelve confusa o salta pasos
3. Hacer 2 preguntas que un principiante haría

Si mi explicación es clara y completa, dilo. Si no, dime qué parte necesito re-estudiar.
```

---

## Devil's Advocate — Preparar Defensas

**Cuándo**: Para preparar ensayos argumentativos o debates

```
Actúa como abogado del diablo sobre [TESIS/ARGUMENTO].
Dame:
1. Los 3 contraargumentos más fuertes contra mi posición
2. Para cada uno, sugiere cómo podría refutarlo o incorporarlo (qualifier)
3. Identifica si mi argumento comete alguna falacia (ad hominem, straw man, false dichotomy, appeal to authority)

Sé riguroso. No me des la razón fácilmente.
```

---

## Chain of Density — Resumen Progresivo

**Cuándo**: Para generar un resumen denso de un tema largo

```
Resume [TEMA] en 5 oraciones.
- Oración 1: Contexto general (accesible para cualquiera)
- Oración 2: Agrega 1-2 conceptos técnicos clave
- Oración 3: Agrega más densidad (relaciones causales, datos)
- Oración 4: Máxima densidad (fórmulas, modelos, autores)
- Oración 5: Implicación práctica o conclusión

Cada oración debe ser más densa e informativa que la anterior, sin repetir información.
```

---

## Socratic Tutor — Guiar sin Dar Respuesta

**Cuándo**: Cuando el usuario tiene una duda pero se quiere forzar a pensar

```
Actúa como un tutor socrático. El estudiante tiene esta duda: [DUDA].
NO le des la respuesta directa. En cambio:
1. Haz una pregunta que lo guíe hacia la respuesta
2. Si responde parcialmente, haz otra pregunta más específica
3. Solo revela la respuesta si después de 3 rondas no la encuentra

El objetivo es que el estudiante DESCUBRA la respuesta, no que la reciba.
```

---

## Exam Simulator — Mini-Examen Oral

**Cuándo**: Modo Crisis, preparación pre-examen

```
Actúa como profesor universitario de [CURSO].
Hazme un mini-examen oral de 5 preguntas sobre [TEMA]:
- 2 preguntas conceptuales (comprensión)
- 2 preguntas de aplicación (resolver un caso)
- 1 pregunta de síntesis (conectar múltiples conceptos)

Después de cada respuesta, evalúa si es correcta, parcial, o incorrecta.
Al final, dame una nota del 1 al 20 y qué debo reforzar.
```
