---
name: elite-skill-architect
description: Meta-skill unificada para crear, auditar, mejorar e implementar skills de Brain OS con estándares de calidad profesional. Combina diseño estratégico (auditoría, entrevistas, prompts maestros) con implementación técnica (estructura SKILL.md, scripts, references, assets, Progressive Disclosure). Usar cuando el usuario diga "Quiero crear una skill", "Audita la skill [nombre]", "Evalúa [nombre]", "Score de [nombre]", "Rehace la skill [nombre]", "Mejora [nombre]", "Actualiza [nombre]", "Lista todas las skills", "Compara [skill1] vs [skill2]", "¿Qué skill debería crear?", "Implementa la skill [nombre]".
trigger_conditions:
  - "Quiero crear una skill"
  - "Audita la skill [nombre]"
  - "Rehace la skill [nombre]"
  - "Implementa la skill [nombre]"
  - "Lista todas las skills"
  - "Compara [skill1] vs [skill2]"
  - "¿Qué skill debería crear?"
usage_constraints: "Solo para operaciones sobre skills de Brain OS (crear, auditar, mejorar, implementar). No usar para crear código general o documentación fuera del sistema de skills."
category: "Sistema"
parameters:
  skill_name: "Nombre de la skill objetivo (string, opcional para modo Crear)"
  mode: "Modo de operación: crear | auditar | rehacer | implementar (inferido del comando)"
---

# 🏗️ Elite Skill Architect

> Meta-skill conversacional que crea, audita y mejora skills de Brain OS con calidad de élite.

## Modos de Operación

| Modo | Trigger | Qué Hace |
|------|---------|----------|
| 🆕 Crear | "Quiero crear una skill" | Entrevista 5-7 preguntas → prompt maestro ~2500 palabras |
| 🔍 Auditar | "Audita la skill [nombre]" | Checklist 100 pts → score + brechas |
| 🔄 Rehacer | "Rehace la skill [nombre]" | Entrevista breve → mejora incremental preservando lo bueno |
| 🛠️ Implementar | "Implementa la skill [nombre]" | Crea directorio, SKILL.md, scripts, references, assets |

### Comandos Completos

```
# MODO 1: Crear
"Quiero crear una skill"
"Ayúdame a diseñar una skill"
"Nueva skill para [propósito]"

# MODO 2: Auditar
"Audita la skill [nombre]"
"Evalúa la skill [nombre]"
"Score de [nombre]"
"¿Qué tan buena es la skill [nombre]?"
"Audita todas las skills"

# MODO 3: Rehacer
"Rehace la skill [nombre]"
"Mejora la skill [nombre]"
"Actualiza [nombre]"
"Arregla [nombre]"

# MODO 4: Implementar
"Implementa la skill [nombre]"
"Crea la skill [nombre]"
"Genera la estructura de [nombre]"

# Utilidades
"Lista todas las skills"
"Compara [skill1] vs [skill2]"
"¿Qué skill debería crear?"
```

---

## 🆕 MODO 1: Crear Nueva Skill

### Flujo Completo

```
FASE 1 → Contexto Inicial
  Pregunta: "¿Qué problema quieres resolver con esta skill?"
  Inferir: categoría probable, complejidad estimada

FASE 2 → Alcance
  Pregunta: "¿Qué debería poder hacer? Dame 2-3 ejemplos de uso real"
  Inferir: comandos naturales, inputs/outputs esperados

FASE 3 → Usuarios y Frecuencia
  Pregunta: "¿Con qué frecuencia la usarías? ¿Diario, semanal, bajo demanda?"
  Inferir: si necesita integración con system-coordinator, si debe aparecer en "Buenos días"

FASE 4 → Integraciones
  Pregunta: "¿Necesita conectarse con algo? (Notion, archivos locales, APIs, otras skills)"
  Inferir: dependencias, zonas protegidas, formato de datos

FASE 5 → Riesgos
  Pregunta: "¿Hay algo que esta skill NO debería tocar o modificar?"
  Inferir: zonas críticas, necesidad de rollback, nivel de confirmación

FASE 6 → Refinamiento (opcional)
  Pregunta contextual basada en brechas detectadas en respuestas anteriores
  Inferir: ajustes finales, prioridades del usuario
```

### Inferencias Automáticas

A partir de las respuestas, el architect infiere sin preguntar:

| Dato | Fuente de Inferencia |
|------|---------------------|
| Nombre técnico (`kebab-case`) | Del propósito descrito |
| Categoría (sistema/académica/util) | Del problema que resuelve |
| Nivel de riesgo (🟢/🟡/🔴) | De las zonas que toca |
| Necesidad de scripts Python | Si involucra archivos/APIs/cálculos |
| Necesidad de rollback | Si modifica datos existentes |
| Integración con coordinator | Si es frecuente o core |

### Generación del Prompt Maestro

Después de la entrevista, generar prompt de ~2500 palabras siguiendo la estructura en `references/prompt-templates.md` (Template de Creación).

El prompt generado es autocontenido — el usuario puede dárselo a cualquier agente para implementar la skill completa.

---

## 🔍 MODO 2: Auditar Skill Existente

### Flujo de Auditoría

```
PASO 1 → Localizar skill
  Ruta: skills/{nombre}/
  Leer: SKILL.md, *.py (si existe), scripts/ (si existe)

PASO 2 → Verificar integraciones
  Buscar en: skills/system-coordinator/SKILL.md → ¿mencionada?
  Buscar en: README.md → ¿tiene entrada?

PASO 3 → Evaluar con checklist 100 pts
  Usar checklist completo de references/checklist.md
  Puntuar cada categoría

PASO 4 → Generar reporte
  Formato: Score + barras + brechas priorizadas + recomendación

PASO 5 → Ofrecer acción
  Si score < 60: "¿Quieres que la rehaga?"
  Si score 60-84: "¿Quieres que la mejore?"
  Si score ≥ 85: "Skill de élite. Mejoras menores opcionales: [lista]"
```

### Formato de Reporte de Auditoría

```markdown
╔══════════════════════════════════════╗
║  📊 AUDITORÍA: {nombre_skill}       ║
╚══════════════════════════════════════╝

## Score por Categoría

║  FUNCIONALIDAD:    X/40  [██████░░░]  ║
║  DOCUMENTACIÓN:    X/25  [████░░░░░]  ║
║  INTEGRACIÓN:      X/20  [██████░░░]  ║
║  UX:               X/10  [████░░░░░]  ║
║  SEGURIDAD:        X/5   [████░░░░░]  ║
║  ─────────────────────────────────    ║
║  TOTAL:           XX/100              ║

**Interpretación:**
- 90-100: Elite 🏆
- 75-89: Excelente ⭐
- 60-74: Buena ✅
- 40-59: Necesita mejoras 🔧
- <40: Rehacer recomendado 🚨

## Brechas Detectadas

### 🔴 CRÍTICAS (bloquean funcionalidad)
1. [Brecha] — Impacto: [X] — Acción: [Y]

### 🟡 MEDIAS (reducen calidad)
2. [Brecha] — Impacto: [X] — Acción: [Y]

### 🟢 MENORES (cosméticas)
3. [Brecha] — Impacto: [X] — Acción: [Y]

## Recomendación
[Según score: ÉLITE / EXCELENTE / BUENA / MEJORAR / REHACER]
```

Para el checklist completo de 100 puntos con todos los criterios detallados, ver `references/checklist.md`.

### Auditoría Completa del Sistema

Cuando el usuario dice "Audita todas las skills":

```
PASO 1 → Escanear skills/ → listar directorios con SKILL.md
PASO 2 → Auditar cada una (score rápido, no reporte completo)
PASO 3 → Generar ranking ordenado por score
PASO 4 → Priorizar: ¿cuáles rehacer primero? (menor score + mayor uso)
```

---

## 🔄 MODO 3: Rehacer/Actualizar Skill

### Límite de Iteraciones

> **Regla v2.2**: El bucle Crítica → Refinamiento tiene un **máximo de 5 iteraciones**.
> En la iteración 5, el agente **detiene el bucle**, presenta la mejor versión alcanzada junto con el feedback no resuelto, y solicita aprobación humana antes de continuar.

### Flujo de Re-implementación

```
PASO 1 → Análisis de lo existente
  Leer SKILL.md + código + integraciones
  Usar auditoría previa si existe (evitar re-evaluar)
  Identificar: qué PRESERVAR vs qué MEJORAR

PASO 2 → Entrevista de Mejora (2-3 preguntas)

  P1: "¿Qué funciona bien que DEBEMOS MANTENER?"
      (comandos, lógica principal, integraciones)

  P2: "De las brechas detectadas, ¿cuáles son MÁS IMPORTANTES?"
      [Lista las brechas con números para priorizar]

  P3: "¿Quieres agregar capacidades NUEVAS, o solo mejorar lo existente?"

PASO 3 → Generación del Prompt de Re-implementación
  Seguir template en references/prompt-templates.md (Template de Rehecho)
  Incluir: backup obligatorio + preservar lo bueno + mejorar brechas

PASO 4 → Bucle Crítica → Refinamiento (máx. 5 iteraciones)
  Por cada iteración:
    4a. Generar versión mejorada
    4b. Auto-crítica: ¿se resolvieron las brechas priorizadas?
    4c. Si quedan brechas Y iteración < 5 → refinar y volver a 4a
    4d. Si iteración == 5 → DETENER. Ir a Paso 5.

PASO 5 → Entrega Final
  Si se completó antes de iteración 5:
    Entregar versión final + reporte de mejoras.
  Si se alcanzó iteración 5 (escalamiento):
    Presentar la MEJOR versión alcanzada.
    Listar feedback NO resuelto.
    Solicitar aprobación humana: "¿Apruebas esta versión o quieres guiar el refinamiento?"

PASO 6 → Comparación Antes/Después
  Si se re-audita después de implementar las mejoras:
  Generar delta: score_antes → score_después (+N pts)
```

### Regla de Backup OBLIGATORIA

```
ANTES de cualquier modificación:
1. Crear skills/{nombre}/backup_v{N}/
2. Copiar TODO el contenido actual
3. Confirmar que el backup existe
4. SOLO ENTONCES proceder con cambios
```

---

## Política de Escalamiento

> **Añadido en Brain OS 2.2** — Mecanismo para evitar bucles infinitos de refinamiento.

| Situación | Acción |
|-----------|--------|
| Iteración < 5, brechas resueltas | Entregar versión final normalmente |
| Iteración < 5, brechas pendientes | Continuar refinamiento automático |
| Iteración == 5, brechas pendientes | **DETENER** bucle. Presentar mejor versión + feedback no resuelto. Solicitar decisión humana. |
| Usuario aprueba en iteración 5 | Cerrar con versión actual. Registrar brechas como "aceptadas". |
| Usuario rechaza en iteración 5 | El usuario guía manualmente el siguiente refinamiento (el agente no itera solo). |

### Justificación

El límite de 5 iteraciones previene:
- **Context Rot**: degradación de calidad por acumulación de contexto en el bucle.
- **Diminishing Returns**: después de 5 ciclos, las mejoras marginales rara vez justifican el costo computacional.
- **Loop sin convergencia**: algunos problemas de diseño requieren input humano, no más iteraciones automáticas.

---

## Integración con System Coordinator

El architect reporta cuando se ejecuta "Verifica el sistema completo":

```markdown
🏗️ Elite Skill Architect:
  Skills auditadas esta sesión: X
  Score promedio del sistema: XX/100
  Skills que necesitan mejora: X ([nombre]: XX/100, ...)
  Recomendación: Ejecuta "Rehace la skill [nombre]"
```

> **Nota**: El architect es bajo demanda — no aparece en auditorías automáticas diarias, solo cuando se invoca explícitamente o durante "Verifica el sistema completo".

---

## 🛠️ MODO 4: Implementar Skill (Estructura Técnica)

### Anatomía de una Skill

```
skill-name/
├── SKILL.md                    (obligatorio)
│   ├── Frontmatter YAML        (name + description)
│   └── Instrucciones Markdown
└── Recursos Opcionales/
    ├── scripts/                ← Código ejecutable (Python/Bash)
    ├── references/             ← Documentación para cargar en contexto
    └── assets/                 ← Archivos de salida (templates, imágenes)
```

### Reglas del Frontmatter

| Campo | Obligatorio | Función |
|-------|:-----------:|---------|
| `name` | ✅ | Nombre en kebab-case |
| `description` | ✅ | Trigger de activación — describir QUÉ hace y CUÁNDO usarla |

> **Crítico**: La `description` es lo ÚNICO que el agente lee para decidir si activa la skill. Debe incluir triggers en español.

### Progressive Disclosure (3 Niveles)

1. **Metadata** (~100 palabras) — Siempre en contexto
2. **SKILL.md body** (<500 líneas) — Se carga cuando se activa
3. **Resources** (ilimitado) — Se carga bajo demanda

> **Regla**: Si SKILL.md excede 500 líneas, dividir contenido en `references/`.

### Flujo de Implementación

```
PASO 1 → Crear directorio skills/{nombre}/
PASO 2 → Crear SKILL.md con frontmatter + instrucciones
PASO 3 → Si necesita scripts → crear scripts/
PASO 4 → Si necesita documentación auxiliar → crear references/
PASO 5 → Si necesita templates/imágenes → crear assets/
PASO 6 → Verificar que funciona (dry run)
PASO 7 → Registrar en system-coordinator si es core
```

### Cuándo Usar Cada Tipo de Recurso

| Recurso | Cuándo | Ejemplo |
|---------|--------|---------|
| `scripts/` | Código que se reescribe frecuentemente o necesita ser determinístico | `scripts/cleanup.py`, `scripts/sync.py` |
| `references/` | Documentación que el agente consulta durante el trabajo | `references/api_docs.md`, `references/checklist.md` |
| `assets/` | Archivos usados en el output, no para leer | `assets/template.docx`, `assets/logo.png` |

### Qué NO Incluir

- ❌ `README.md` (la skill es para el agente, no para humanos)
- ❌ `CHANGELOG.md`, `INSTALLATION_GUIDE.md`
- ❌ Documentación de proceso (solo resultado final)
- ❌ Tests unitarios (la verificación va en SKILL.md como escenarios)

---

## Archivos de la Skill

```
skills/elite-skill-architect/
├── SKILL.md                              ← Este archivo
└── references/
    ├── checklist.md                      ← Checklist 100 pts detallado
    └── prompt-templates.md               ← Templates de generación de prompts
```

> **Nota**: Esta skill absorbe las capacidades de la antigua `skill-creator` (archivada en `_archive/skill-creator/`).

---

## 💬 Ejemplos de Interacción

### Ejemplo 1: Auditoría rápida

```
Usuario: "Audita la skill pomodoro"

Agente:
# 🔍 Auditoría: pomodoro — 82/100 ⭐ Excelente

| Categoría       | Score  |
|-----------------|:------:|
| Funcionalidad   | 35/40  |
| Documentación   | 20/25  |
| Integración     | 16/20  |
| UX              | 8/10   |
| Seguridad       | 3/5    |

**Fortalezas**: 5 modos adaptativos, Active Recall, JSON outputs.
**Brechas**: Falta error handling documentado (-5), solo 1 ejemplo (-3).
**Recomendación**: Agregar ≥2 ejemplos y sección de manejo de errores.

¿Quieres que la rehaga o que corrija las brechas específicas?
```

### Ejemplo 2: Creación de skill nueva

```
Usuario: "Quiero crear una skill para notificaciones de WhatsApp"

Agente: Perfecto, voy a entrevistarte para diseñar la skill.

1. ¿Cuál es el PROBLEMA principal que resuelve?
   → "Quiero recibir alertas de tareas próximas por WhatsApp"

2. ¿QUIÉN la usará y en qué CONTEXTO?
   → "Yo, como parte del flujo matutino de Buenos Días"

3. ¿Qué HERRAMIENTAS/APIs necesita?
   → "La API de WhatsApp Business o Twilio"

4. ¿Cómo se ACTIVA? (triggers)
   → "Cuando diga 'Enviar recordatorio' o automáticamente en Buenos Días"

5. ¿Qué OUTPUTS esperas?
   → "Un mensaje de WhatsApp con las 3 tareas más urgentes"

[Agente genera prompt maestro de ~2500 palabras...]
[Agente pregunta si quiere implementar con Modo 4...]
```

---

## 🧪 Escenarios de Prueba

### Test 1: Auditoría genera score correcto

```
Input:    "Audita la skill brainstorming"
Espera:   Score numérico /100 con desglose por 5 categorías
Verifica: - Score entre 0-100
          - Todas las categorías suman el total
          - Identifica al menos 1 fortaleza y 1 brecha
Output:   Tabla + fortalezas + brechas + recomendación
```

### Test 2: Auditoría masiva produce ranking

```
Input:    "Audita todas las skills"
Espera:   Tabla ordenada de mayor a menor score
Verifica: - Cada skill tiene score /100 y nivel (Elite/Excelente/Buena/Mejorar)
          - Score promedio calculado correctamente
Output:   Ranking + score promedio + top 3 + bottom 3
```

### Test 3: Creación inicia entrevista

```
Input:    "Quiero crear una skill"
Espera:   Inicia entrevista con primera pregunta
Verifica: - NO genera SKILL.md sin completar entrevista
          - Pregunta se enfoca en el PROBLEMA
Output:   Pregunta 1 de 5-7
```

### Test 4: Rehacer preserva funcionalidad

```
Input:    "Rehace la skill library-manager"
Espera:   Lee SKILL.md actual ANTES de modificar
Verifica: - Crea backup en _archive/
          - Preserva comandos y flujos existentes
          - Expande documentación sin eliminar contenido
Output:   SKILL.md mejorado + nota de backup
```

### Test 5: Implementar genera estructura completa

```
Input:    "Implementa la skill whatsapp-alerts"
Espera:   Crea directorio con SKILL.md + subdirectorios necesarios
Verifica: - skills/whatsapp-alerts/SKILL.md existe
          - Frontmatter tiene name + description con triggers
          - Description incluye triggers en español
Output:   "Skill whatsapp-alerts creada con éxito" + estructura
```
