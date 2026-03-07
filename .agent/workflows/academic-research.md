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

**Reglas para queries**: Específicas con operadores Scholar (comillas, rango de años). Mínimo 5, máximo 8.
- ❌ Genéricas: `"study methods economics"`
- ✅ Específicas: `"Pomodoro technique academic performance university students" 2020..2026`

---

### Paso 3 — Creación del Notebook y Checkpoint de Fuentes

5. **Crear el notebook nuevo** automáticamente:
   ```bash
   cd skills/notebooklm
   python scripts/run.py create_notebook.py --name "research-[tema]-[año]"
   ```
   Si falla (UI cambió), modo manual:
   ```bash
   python scripts/run.py create_notebook.py --name "research-[tema]-[año]" --manual
   ```
   Mostrar al usuario:
   ```
   ✅ Notebook creado: research-[tema]-[año]
   🔗 URL: https://notebooklm.google.com/notebook/[id]

   Abre este link y sube los PDFs que encontraste.
   Dime "listo" cuando hayas terminado.
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
> **Queries detalladas**: Ver `.agent/workflows/academic-research-queries.md`

Ejecutar en orden: **Ronda 1 → Ronda 2 (según purpose) → Ronda 3 → Ronda 4**

| Ronda | Queries | Objetivo | Siempre |
|-------|---------|----------|---------|
| 1 — Panorama | 2 | Mapa completo del notebook | ✅ Sí |
| 2 — Disección | 3-5 | Adaptar al purpose diagnosticado | Según purpose |
| 3 — Desafío | 2-5 | Críticas, contradicciones, gaps | ✅ Sí |
| 4 — Extracción | 1-2 | Output accionable final | ✅ Sí |

> **Nota de eficiencia**: Si Ronda 1 revela ≤3 fuentes con poco contenido, saltar directo a Ronda 4.

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

Si `purpose = brain-os`, la especificación técnica es el **output principal**; los hallazgos clave son contexto de justificación.

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
/brain-os-dev   → detecta necesidad → /academic-research → hallazgos → continúa dev
/brain-os-study → tarea compleja   → /academic-research → fundamento → continúa tarea
Standalone      → usuario pide investigar → /academic-research → síntesis final
```

---

## Notas

- Los notebooks de investigación se distinguen por la convención `research-*` en su ID
- Consultar `config/research_log.json` antes de iniciar para evitar duplicar trabajo
- Límite de NotebookLM: 50 queries/día — administrar con criterio
- Queries completas del Paso 4 en: `.agent/workflows/academic-research-queries.md`
- Este workflow complementa a `research-engineer` (rigor formal) y `last30days` (actualidad)
