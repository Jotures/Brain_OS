---
description: Referencia de queries para el Paso 4 del workflow /academic-research (Protocolo de Interrogación Profunda).
---

# 📋 Queries del Protocolo de Interrogación Profunda

> Archivo de referencia para el **Paso 4** de `/academic-research`.
> Máximo 12 queries por sesión. Reemplaza `[URL]` con la URL real del notebook.

---

## Ronda 1 — Panorama (siempre se ejecuta, 2 queries)

```bash
cd skills/notebooklm

# Q1: Mapa exhaustivo de todas las fuentes
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Resume ALL the main findings, conclusions and recommendations from EVERY source in this notebook. Include author names. Be comprehensive and exhaustive."

# Q2: Detectar las piezas de oro
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "What are the most surprising or counterintuitive findings across all sources? What challenges conventional wisdom or what is the most novel contribution?"
```

---

## Ronda 2 — Disección por Purpose (3-5 queries, adaptativas)

### SI `purpose = brain-os`

```bash
# B-2a: Parámetros implementables
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué valores NUMÉRICOS específicos recomiendan los autores? Duraciones, intervalos, frecuencias, ratios, porcentajes. Dame los NÚMEROS EXACTOS con la fuente de cada uno."

# B-2b: Comparaciones cuantitativas
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Hay comparaciones cuantitativas entre variantes o métodos? (ej: 25min vs 50min, 3 repeticiones vs 5). ¿Cuál gana, por cuánto, y en qué contexto?"

# B-2c: Arquitectura y flujos
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué frameworks, modelos, ciclos o arquitecturas proponen los autores para organizar [el sistema en cuestión]? Describe CADA FASE con su duración y criterio de transición a la siguiente."

# B-2d: Adaptación por tipo de tarea
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Los resultados cambian según el TIPO DE TAREA? (creativa vs analítica vs memorización vs resolución de problemas). ¿Cómo debería adaptarse el sistema según la tarea?"

# B-2e: Factores contextuales
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Los resultados cambian por nivel de fatiga, hora del día, experiencia previa del usuario, o carga cognitiva? ¿Qué adaptaciones sugieren los autores?"
```

### SI `purpose = tarea-académica`

```bash
# A-2a: Supuestos del modelo
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Cuáles son los supuestos fundamentales del modelo o teoría principal? ¿Qué pasa si se violan? ¿Son realistas según los propios autores?"

# A-2b: Evidencia empírica
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué evidencia empírica presentan los autores? Detalla: países, períodos, tamaño de muestra, metodología utilizada y variables principales."

# A-2c: Comparación entre enfoques
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Cómo se comparan los diferentes modelos o enfoques según los autores? ¿Cuáles son las ventajas y desventajas de cada uno?"

# A-2d: Datos estadísticos
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué datos estadísticos concretos citan los autores? Coeficientes, elasticidades, tasas, porcentajes. ¿De qué fuentes primarias vienen?"

# A-2e: Recomendaciones de política
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué recomendaciones de política o acción proponen los autores? ¿Con qué justificación teórica y empírica?"
```

### SI `purpose = ensayo`

```bash
# E-2a: Posiciones opuestas
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué posturas opuestas existen sobre este tema? Dame los argumentos MÁS FUERTES de cada lado con citas directas de los autores."

# E-2b: Diálogo entre autores
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué autores del notebook citan o responden a otros autores del mismo notebook? ¿Cómo dialogan entre sí? ¿Hay una progresión del debate?"

# E-2c: Estado actual del debate
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Cuál es la postura más reciente o actualizada y en qué se diferencia de las anteriores? ¿El debate está resuelto o sigue abierto?"

# E-2d: Revisiones sistemáticas
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Hay meta-análisis o revisiones sistemáticas entre las fuentes? ¿Qué concluyen sobre el estado general del conocimiento en este tema?"
```

---

## Ronda 3 — Desafío (siempre se ejecuta, 2-5 queries)

```bash
# D-3a: Críticas más fuertes
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Based on ALL sources: what are the STRONGEST criticisms, limitations, and weaknesses of these findings? What would a skeptic say?"

# D-3b: Lo que falta
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué dicen los autores que FALTA investigar? ¿Qué preguntas dejan sin responder? ¿Qué sigue sin estar probado?"

# D-3c: Contradicciones
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Hay contradicciones ENTRE las fuentes? ¿Dónde discrepan los autores y a qué se debe la discrepancia?"
```

**Adicional SI `purpose = brain-os`:**

```bash
# D-3d: Anti-patrones
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué implementaciones o enfoques similares FALLARON según los autores? ¿Qué anti-patrones debo EVITAR? ¿Por qué fracasaron?"

# D-3e: Sostenibilidad temporal
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿El sistema/técnica sigue funcionando después de semanas o meses de uso? ¿Se degrada con el tiempo? ¿Qué hacen para mantener la efectividad a largo plazo?"
```

---

## Ronda 4 — Extracción de Valor (1-2 queries, cierre)

**SI `purpose = brain-os`:**
```bash
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Based on ALL the evidence in this notebook: write a TECHNICAL SPECIFICATION for implementing [feature/sistema] for a university economics student. Include: exact parameters with values, phases of the system with durations, conditions for when to adapt, anti-patterns to avoid, and metrics to measure success. Be as specific and implementable as possible."
```

**SI `purpose = tarea-académica`:**
```bash
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Provide a comprehensive structured summary with author names, years, and key findings from EVERY source. Format each finding ready for APA 7 citation. Group by theme or chronology."
```

**SI `purpose = ensayo`:**
```bash
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "What is the STRONGEST, most well-supported argument you can construct from these sources in support of [tesis del ensayo]? Use direct quotes where possible and cite every claim."
```

---

> **Nota de eficiencia**: Si Ronda 1 revela ≤3 fuentes con poco contenido, saltar directo a Ronda 4. Si las fuentes son ricas, ejecutar las 4 rondas completas.
