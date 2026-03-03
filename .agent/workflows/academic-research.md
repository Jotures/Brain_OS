---
description: Workflow de investigación académica profunda via NotebookLM. Auto-activado por el agente cuando detecta tareas de alta complejidad que requieren sustento teórico con fuentes verificables. Siempre pide confirmación antes de iniciar.
---

# 🔬 Workflow de Investigación Académica — `/academic-research`

Protocolo de investigación que usa NotebookLM como motor de búsqueda semántica sobre fuentes académicas reales (PDFs, papers, libros).

**Quién lo activa**: El agente, cuando detecta que la tarea actual lo requiere.
**Cuándo se activa**: Tareas de alta complejidad con necesidad de sustento teórico.

---

## Criterios de Activación

El agente evalúa estos criterios y, si ≥2 se cumplen, **propone** activar el workflow:

```
✅ La tarea requiere justificación teórica (no solo práctica)
✅ Se necesita mejorar Brain OS basándose en evidencia
✅ Trabajo académico con peso ≥ 30% de la nota
✅ El usuario pide explícitamente fuentes o investigación
✅ El diseño propuesto se beneficiaría de estado del arte
```

> ⚠️ **OBLIGATORIO**: Siempre pedir confirmación antes de iniciar.
> Formato: "Detecto que esta tarea se beneficiaría de investigación académica. ¿Activo el workflow de investigación? Esto implica que busques y subas papers a un notebook nuevo en NotebookLM."

---

## Los 7 Pasos

### Paso 1 — Diagnóstico y Confirmación

1. **Evaluar criterios** de activación (lista de arriba).
2. **Pedir confirmación** al usuario con el formato obligatorio.
3. **Diagnosticar**:
   ```
   ¿Qué se investiga? → [tema específico]
   ¿Para qué?         → brain-os | tarea-académica | ensayo
   ¿Profundidad?      → overview | análisis | estado-del-arte
   ```

**Si el usuario rechaza → no continuar. Resolver la tarea sin este workflow.**

---

### Paso 2 — Briefing de Búsqueda Académica

// turbo
4. **Generar brief de búsqueda** con este formato exacto:

```
📚 BRIEFING DE INVESTIGACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━

Tema: [tema]
Propósito: [brain-os | académico | ensayo]
Notebook propuesto: research-[tema-corto]-[año]

🔍 QUERIES RECOMENDADAS (copiar y pegar en Google Scholar):

1. "[query en inglés con operadores]"
   → Busca: [qué esperas encontrar]

2. "[query en inglés]"
   → Busca: [qué esperas encontrar]

3. "[query en español si aplica]"
   → Busca: [contexto local/regional]

4-8. [más queries según complejidad]

📋 CRITERIOS DE SELECCIÓN:
- Priorizar: systematic review > meta-analysis > empirical study
- Años: [rango recomendado, ej. 2019-2026]
- Mínimo: 3-5 fuentes para overview, 8-12 para estado del arte
- Idioma: inglés (más resultados) + español (contexto local)

🔗 DÓNDE BUSCAR:
- Google Scholar: scholar.google.com
- arXiv: arxiv.org (si aplica a ciencias exactas)
- Semantic Scholar: semanticscholar.org
- Scielo: scielo.org (papers latinoamericanos)

📝 INSTRUCCIONES:
1. Crea un notebook nuevo en NotebookLM llamado "research-[tema]-[año]"
2. Sube los PDFs encontrados como fuentes
3. Dime "listo" y pega la URL del notebook
```

**Reglas para generar queries**:
- ❌ Genéricas: `"study methods economics"`
- ✅ Específicas: `"Pomodoro technique academic performance university students" 2020..2026`
- Incluir operadores de Scholar: comillas, rango de años, `site:`
- Mínimo 5 queries, máximo 8

---

### Paso 3 — Creación del Notebook y Checkpoint de Fuentes

5. **Crear el notebook nuevo** automáticamente:
   ```bash
   cd skills/notebooklm
   python scripts/run.py create_notebook.py --name "research-[tema]-[año]"
   ```

   Si falla (UI cambió), usar modo fallback con browser visible:
   ```bash
   python scripts/run.py create_notebook.py --name "research-[tema]-[año]" --show-browser
   ```

   El script devuelve la URL del notebook. Mostrarla al usuario:
   ```
   ✅ Notebook creado: research-[tema]-[año]
   🔗 URL: https://notebooklm.google.com/notebook/[id]
   
   Abre este link y sube los PDFs que encontraste con las queries del briefing.
   Dime "listo" cuando hayas terminado de subir las fuentes.
   ```

6. **Esperar** hasta que el usuario diga "listo" / "ya subí" / "ya están".
   **No continuar hasta recibir confirmación explícita.**

7. **Registrar el notebook nuevo**:
   ```bash
   cd skills/notebooklm
   python scripts/run.py notebook_manager.py add \
     --url "[URL del notebook]" \
     --name "research-[tema]-[año]" \
     --description "Investigación: [tema completo]" \
     --topics "[keywords del tema]"
   ```

---

### Paso 4 — Protocolo de Interrogación Profunda

> **Principio**: No salir del notebook hasta tener respuestas que cambien cómo pienso sobre el problema.
> **Límite**: Máximo 12 queries por sesión (~24% del presupuesto diario de NotebookLM).

```bash
cd skills/notebooklm
```

---

#### Ronda 1 — Panorama (2 queries, siempre se ejecuta)

Objetivo: Mapear el contenido completo antes de profundizar.

```bash
# Q1: Mapa exhaustivo de todas las fuentes
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Resume ALL the main findings, conclusions and recommendations from EVERY source in this notebook. Include author names. Be comprehensive and exhaustive."

# Q2: Detectar las piezas de oro
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "What are the most surprising or counterintuitive findings across all sources? What challenges conventional wisdom or what is the most novel contribution?"
```

Tras la Ronda 1, el agente tiene un mapa mental completo del notebook. Las siguientes preguntas se construyen basándose en estas respuestas — no son fijas.

---

#### Ronda 2 — Disección por Purpose (3-5 queries, adaptativas)

Las preguntas se eligen según el `purpose` diagnosticado en el Paso 1.

**SI `purpose = brain-os`** (mejora del sistema):

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

**SI `purpose = tarea-académica`**:

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

**SI `purpose = ensayo`**:

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

#### Ronda 3 — Desafío (2-5 queries, siempre se ejecuta)

Objetivo: Encontrar debilidades, fracasos y contradicciones para no quedarme con una visión sesgada.

```bash
# D-3a: Críticas más fuertes
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Based on ALL sources: what are the STRONGEST criticisms, limitations, and weaknesses of these findings? What would a skeptic say?"

# D-3b: Lo que falta
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué dicen los autores que FALTA investigar? ¿Qué preguntas dejan sin responder? ¿Qué sigue sin estar probado?"

# D-3c: Contradicciones
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Hay contradicciones ENTRE las fuentes? ¿Dónde discrepan los autores y a qué se desbe la discrepancia?"
```

**Adicional SI `purpose = brain-os`**:

```bash
# D-3d: Anti-patrones
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿Qué implementaciones o enfoques similares FALLARON según los autores? ¿Qué anti-patrones debo EVITAR? ¿Por qué fracasaron?"

# D-3e: Sostenibilidad temporal
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "¿El sistema/técnica sigue funcionando después de semanas o meses de uso? ¿Se degrada con el tiempo? ¿Qué hacen para mantener la efectividad a largo plazo?"
```

---

#### Ronda 4 — Extracción de Valor (1-2 queries, según purpose)

La pregunta de cierre que convierte todo en output accionable.

**SI `purpose = brain-os`**:
```bash
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Based on ALL the evidence in this notebook: write a TECHNICAL SPECIFICATION for implementing [feature/sistema] for a university economics student. Include: exact parameters with values, phases of the system with durations, conditions for when to adapt, anti-patterns to avoid, and metrics to measure success. Be as specific and implementable as possible."
```

**SI `purpose = tarea-académica`**:
```bash
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "Provide a comprehensive structured summary with author names, years, and key findings from EVERY source. Format each finding ready for APA 7 citation. Group by theme or chronology."
```

**SI `purpose = ensayo`**:
```bash
python scripts/run.py ask_question.py --notebook-url "[URL]" \
  --question "What is the STRONGEST, most well-supported argument you can construct from these sources in support of [tesis del ensayo]? Use direct quotes where possible and cite every claim."
```

---

> **Nota sobre eficiencia**: Si la Ronda 1 revela que el notebook tiene pocas fuentes  (≤3) y poco contenido, se puede comprimir saltando de Ronda 1 directo a Ronda 4.  Pero si las fuentes son ricas, ejecutar las 4 rondas completas. El criterio es siempre  extraer el máximo impacto, no ahorrar queries.

---

### Paso 5 — Síntesis Final

9. **Generar síntesis** con este formato:

```
📊 SÍNTESIS DE INVESTIGACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━

Tema: [tema]
Fuentes consultadas: [N] papers/documentos
Queries realizadas: [N] de 12 máx

🔑 HALLAZGOS CLAVE:
1. [hallazgo con citación] (Autor, Año)
2. [hallazgo] (Autor, Año)
3. [hallazgo] (Autor, Año)
...

⚖️ CONSENSO/DISCREPANCIAS:
[Qué dicen igual vs. diferente los autores]

🚫 LIMITACIONES Y ANTI-PATRONES:
[Qué evitar y por qué, con fuente]

🎯 IMPLICACIONES PARA [tarea original]:
[Cómo aplicar estos hallazgos concretamente]

📚 REFERENCIAS (APA 7):
- Apellido, N. (Año). Título del artículo. Journal, Vol(N), pp-pp.
[Si no hay DOI, citar por título + año]
```

**Adicional SI `purpose = brain-os`** — agregar bloque:
```
🛠️ ESPECIFICACIÓN TÉCNICA:
- Parámetro [X]: [valor exacto] (Fuente: Autor, Año)
- Parámetro [Y]: [valor exacto] (Fuente: Autor, Año)
- Arquitectura: [descripción de fases/ciclo]
- Condiciones de adaptación: [cuándo aplicar qué variante]
- Anti-patrones: [qué evitar y por qué]
- Métrica de éxito: [cómo medir que funciona]
```

Si la investigación es para Brain OS, esta sección de especificación es el **output principal** — los hallazgos clave son contexto para justificarla.

---

### Paso 7 — Registro

// turbo
10. **Registrar** la investigación en `config/research_log.json`:
    ```json
    {
      "id": "research-[tema]-[año]",
      "date": "YYYY-MM-DD",
      "topic": "[tema]",
      "purpose": "brain-os | academic | essay",
      "notebook_url": "[URL]",
      "queries_used": ["query1", "query2", "..."],
      "sources_count": N,
      "findings_summary": "[resumen de 1-2 líneas]"
    }
    ```

---

## Cuándo NO activar este workflow

```
❌ Pregunta simple que se responde con conocimiento general
❌ Tarea de programación que no necesita fundamento teórico
❌ Tareas de peso bajo (< 30% de la nota)
❌ El usuario dice "no" cuando se propone la activación
❌ Ya existe una investigación previa del mismo tema en research_log.json
```

---

## Integración con otros workflows

```
/brain-os-dev → detecta necesidad → /academic-research → hallazgos → continúa dev
/brain-os-study → tarea compleja → /academic-research → fundamento → continúa tarea
Standalone → usuario pide investigar → /academic-research → síntesis final
```

---

## Notas

- Los notebooks de investigación se distinguen por la convención `research-*` en su ID
- Consultar `config/research_log.json` antes de iniciar una investigación nueva para evitar duplicar trabajo
- Límite de NotebookLM: 50 queries/día — administrar con criterio
- Este workflow complementa a `research-engineer` (rigor formal) y `last30days` (actualidad)
