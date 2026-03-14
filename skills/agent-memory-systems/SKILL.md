---
name: agent-memory-systems
description: "Patrones y flujos operativos para gestionar eficientemente la memoria a corto y largo plazo del agente. Usar cuando necesites recordar contexto pasado, manejar los límites del Context Window, investigar el historial de conversaciones previas, o almacenar conocimiento persistente para el futuro en Notion o archivos locales."
---

# 🧠 Agent Memory Systems

> Manual operativo para agentes. La memoria no es solo almacenamiento de datos sin procesar, es **recuperación efectiva** en el momento exacto en que se necesita.

## Cuándo Usar Esta Skill
Actívala proactivamente o cuando el usuario diga:
- *"Recuerda lo que hicimos en la sesión anterior..."*
- *"Guarda esto en tu memoria a largo plazo..."*
- *"Busca en tus notas sobre el tema X..."*
- *"Siento que te olvidaste de las instrucciones iniciales..."*
- *"Resume esta conversación para retomarla mañana..."*

---

## 1. Arquitectura de Memoria en Brain OS

### 1.1 Short-Term Memory (Context Window)
Tu memoria de trabajo actual. Limitada, volátil pero de acceso inmediato y altísimo rendimiento.
- **Nivel de Uso**: Tareas inmediatas y diálogo en la sesión paso-a-paso.
- **Riesgo Operativo**: Si el contexto se llena de archivos inmensos o basura, tu capacidad analítica disminuirá (alucinaciones o "olvidos" de la primera instrucción).
- **Control Activo**: El agente debe ser celoso de lo que admite en su ventana de contexto.

### 1.2 Episodic Memory (Conversation Logs)
Es el recuerdo cronológico de "qué pasó, qué hice, y cuándo".
- **Nivel de Uso**: Para recuperar el hilo de sesiones, scripts temporales generados ayer, o decisiones de diseño tomadas la semana pasada.
- **Soporte**: Carpetas del sistema como el historial de `.agent/logs/`, `config/audit_log.json` o los archivos en `sesiones/`.

### 1.3 Semantic Memory (Long-Term Storage)
Es tu conocimiento persistente, estructurado e indexado del sistema.
- **Nivel de Uso**: Reglas globales, esquemas de bases de datos, resúmenes de cursos universitarios y preferencias del usuario.
- **Soporte**: Notion (BD_TAREAS, BD_RECURSOS vía MCP), NotebookLM (RAG de pdfs) y archivos markdown locales en `skills/`, `docs/` o `config/`.

---

## 2. Patrones Operativos: Gestión del Contexto (Corto Plazo)

### 2.1 Patrón: Progressive Disclosure
No cargues un archivo de 2000 líneas en el contexto si solo necesitas leer una función específica.
- **Flujo**: Usar herramientas como `read_file` especificando `start_line` y `end_line`, o usar `grep_search` para encontrar exactamente dónde está el dato.

### 2.2 Patrón: Context Pruning
Cuando notas que el usuario cambia radicalmente de tema (ej: de programar React a analizar un dataset económico):
- **Acción**: Haz una transición limpia. "Hemos terminado con React. Para optimizar mi memoria, me enfocaré solo en los datos económicos ahora y liberaré las herramientas del código." Esto previene el cruce indeseado de dominios.

### 2.3 Patrón: Hemingway Bridge
La mejor forma de traspasar Short-Term a Long-Term al finalizar un bloque de trabajo antes de cerrar la sesión.
- **Flujo**:
  1. Identifica qué se logró (pasado).
  2. Determina con precisión el *próximo paso bloqueante a retomar* (futuro).
  3. Escribe esto en `config/hemingway_bridge.json` o en `INICIO.md`.
  4. En la próxima sesión, el que inicie podrá leer ese archivo y restaurar el momentum instantáneamente.

### 2.4 Patrón: MaRS — Evicción en Cascada 🆕
> **Fuente**: Memory-Aware Retention Scheme (2024). Activar cuando el contexto supera el `token_budget` configurado en `MEMORY_GOVERNANCE`.

Cuando el contexto empieza a saturarse (señales: respuestas más lentas, pérdida de contexto inicial, repetición de preguntas):
```
FASE 1 — Higiene (O(k), costo bajo):
  → Descartar contexto de temas ya cerrados o irrelevantes al objetivo activo.
  → Priorizar: ¿Esto sigue siendo relevante para la tarea ACTUAL?

FASE 2 — Reflexión Semántica (activar si Fase 1 no basta):
  → Identificar episodios similares o redundantes en el hilo activo.
  → Comprimir: "Los 3 errores de importación de las últimas 10 respuestas" → 1 nota compacta.
  → Avisar: 'He compactado N episodios redundantes para mantener coherencia.'

FASE 3 — Evicción por Prioridad (último recurso):
  → Descartar los fragmentos con menor densidad de importancia (hechos poco citados, old decisions).

FALLBACK — Random Drop (regularizador de emergencia, MaRS research):
  → Si las 3 fases no son suficientes, descartar 1 fragmento aleatorio del hilo.
  → Paradójicamente eficaz: evita que el agente refuerce loops o memorias erróneas.
```

### 2.5 Patrón: AgeMem — Context Clearing Deliberado 🆕
> **Fuente**: AgeMem - Agentic Memory (2024). Reinicio de STM para forzar el uso de LTM.

Para tareas largas donde el agente empieza a ignorar la LTM porque la STM está llena de historia reciente:
```
FASE 1 (T₁) — Exploración con STM:
  → Trabajar normalmente, acumulando contexto de la tarea.
  → El agente registra activamente qué información es 'candidata a LTM'.

FASE 2 (T₂) — Context Clearing:
  → Declarar explícitamente: 'Reinicio de contexto intermedio para optimizar atención.'
  → Guardar en LTM (semantic_memory.json) los gists más importantes de T₁.
  → Recomenzar con contexto limpio, FORZANDO al agente a recuperar desde LTM.

FASE 3 (T₃) — Razonamiento Integrado:
  → Ejecutar la tarea final usando LTM recuperada + contexto fresco.
```
**Trigger recomendado**: Aplicar en sesiones que superan 30 minutos o > 15 turnos.

---

## 3. Patrones Operativos: Recuperación (Medio y Largo Plazo)

### 3.1 Recuperar un Log Pasado (Memoria Episódica)
Si el usuario dice *"Usa el abordaje del script que hicimos ayer"*:
```
PASO 1 → Preguntar / inferir fecha (ej. "Ayer fue 13 de marzo").
PASO 2 → Listar los logs generados por el sistema en su respectivo directorio (por metadata del sistema o archivos locales).
PASO 3 → Usar `grep_search` iterativamente buscando palabras clave.
PASO 4 → Extraer el bloque técnico y usarlo.
```

### 3.2 Almacenar Conocimiento Persistente (Memoria Semántica)
Si tras una tarea deduces una nueva regla sistemática que el usuario aprobó:
```
PASO 1 → ¿Es sobre el comportamiento de programación? → Guardar en las `skills/` pertinentes o en un guidelines.md global.
PASO 2 → ¿Es información teórica de un curso? → Integrarlo a archivos de conocimiento del curso para RAG.
PASO 3 → ¿Es algo a hacer? → Apuntarlo a BD_TAREAS usando Notion MCP.
```

### 3.3 Consolidación Semántica — Ciclo FER (Sueño REM) 🆕
> **Fuente**: CMA - Continuum Memory Architecture (2024-2025). Se ejecuta al cierre de sesión.

Ejecutar **después del Hemingway Bridge** al cerrar cada sesión. Convierte episodios concretos en conocimiento abstracto reutilizable:
```
F — FORMACIÓN (ocurrió durante la sesión):
  → Los episodios están en el episodic log (sesiones/, conversation logs).

E — EVOLUCIÓN (acción activa al cierre):
  PASO 1 → Revisar los 3-5 episodios clave de la sesión.
  PASO 2 → Extraer el gist abstracto: ¿Qué aprendí que vale para FUTURAS sesiones?
  PASO 3 → Escribir en config/semantic_memory.json:
  {
    "date": "YYYY-MM-DD",
    "source_session": "[descripción breve]",
    "gist": "[conocimiento abstracto reutilizable]",
    "confidence": "high|medium|low",
    "domain": "notebooklm|auth|workflow|memoria|etc"
  }

R — RECUPERACIÓN (al inicio de sesiones futuras del mismo dominio):
  → Leer los últimos 5 gists del dominio activo ANTES de leer los conversation logs.
  → Usarlos como contexto de arranque privilegiado.
```

**Ejemplo de gist válido**: `"Motor v2 NotebookLM expira silenciosamente después de 7 días. Usar Motor v1 (Patchright) como fallback o forzar re-auth al inicio."`

---

## 4. ⚠️ Manejo de Errores y Rollback

### 4.1 Problema: Token Limit Exceeded / Degradación de Memoria (Context Rot)
- **Síntoma**: Respuestas más lentas, el agente 'olvida' instrucciones del inicio, repite preguntas ya resueltas (señal de 'lost in the middle').
- **Acción Correctora — Protocolo MaRS**:
  1. Declarar: *"Detecté señales de Context Rot (token_budget ~ 6k). Aplicando evicción MaRS."*
  2. Ejecutar Fase 1 (Higiene): descartar temas cerrados.
  3. Ejecutar Fase 2 (Reflexión): comprimir episodios redundantes.
  4. Si persiste: mini Hemingway Bridge + solicitar nuevo contexto de sesión.
- **NUNCA**: Simplemente continuar sin acción. El deterioro es silencioso y acumulativo.

### 4.2 Problema: Inconsistencia al Escribir al Long-Term
- **Síntoma**: Guardas mal una regla en un archivo SKILL.md base, rompiendo otra regla.
- **Mecanismo de Rollback**: Al igual que dictan los patrones autónomos, *nunca reescribas sin leer primero todo o hacer un backup temporal.* Si el usuario nota que el agente guardó un recuerdo erróneo ("Eso que aprendiste sobre la API está mal"), revierte el cambio en el archivo y descarta la deducción.

---

## 5. UI y Experiencia de Usuario

### 5.1 Outputs Formativos
Cuando se ejecuta explícitamente una acción de memoria a largo plazo, el agente debe mostrar un reporte visual confirmatorio:

```markdown
🧠 **Memoria Actualizada**
- **Destino**: `config/hemingway_bridge.json`
- **Registro clave**: "Dejaste pendiente terminar el test E2E del formulario de Auth de React"
- **Recuperación**: El próximo agente que inicie el día retomará automáticamente desde este punto.
```

---

## 🧪 Escenarios de Prueba Documentados (Tests)

### Test 1: Ingesta Insegura Prevenida
```
Input:    "Voy a pegarte 5 archivos de la base de datos de 10.000 líneas cada uno para que los leamos enteros."
Espera:   El agente reconoce el riesgo de saturar el Context Window y perder calidad cognitiva.
Verifica: Propone usar Progressive Disclosure o `grep_search`.
Output:   "Es mejor que use la herramienta grep para buscar lo que necesitas en vez de leer las 50.000 líneas de golpe, lo que degradaría mi memoria."
```

### Test 2: Hemingway Bridge Correcto
```
Input:    "Haz un Hemingway para terminar el día de trabajo"
Espera:   Agente resume y guarda próximo paso clave sin fricción.
Verifica: Escribe/actualiza en un archivo persistente (ej: `hemingway_bridge.json`).
Output:   Muestra el recuadro formativo `🧠 Memoria Actualizada`.
```

### Test 3: Búsqueda Episódica Fallida
```
Input:    "Busca en las sesiones de enero sobre mi ensayo de Kant"
Espera:   Intenta buscar en historial o archivos, pero no encuentra nada relevante.
Verifica: No inventa ni alucina contenido que no está en la búsqueda.
Output:   "He buscado en los logs episódicos disponibles usando las palabras 'Kant' y 'ensayo', pero no tengo el registro de esa conversación."
```

### Test 4: Regla Persistente Efectiva (Semántica)
```
Input:    "A partir de ahora, recuerda que siempre uso Yarn en este proyecto, no npm"
Espera:   El agente detecta que es necesario llevarlo al almacenamiento a Largo Plazo.
Verifica: Localiza el `Brain_OS_Master_Doc.md` o archivo respectivo e inyecta la regla.
Output:   "He interiorizado esto en tu memoria semántica. Todos mis futuros comandos usarán yarn."
```

### Test 5: Rollback de Contexto por Edición Errónea
```
Input:    El agente resume mal una clase universitaria y sobrescribe el apunte de Notion, el usuario dice: "Recupera lo que borraste, está mal resumido".
Espera:   Aplicación de la política de rollback (tener el estado original de la lectura).
Verifica: Restitución del contenido original usando el backup en memoria corta.
Output:   "Operación revertida exitosamente. El apunte vuelve a su versión anterior."
```
