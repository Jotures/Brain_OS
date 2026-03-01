# 📝 Templates de Generación de Prompts

> Templates que el architect usa para generar prompts maestros después de las entrevistas.

---

## Template 1: Creación de Skill Nueva

Usar después de completar la entrevista de 5-7 preguntas (Modo 1).

```markdown
# 🚀 PROMPT MAESTRO: Implementa la Skill "{nombre_skill}"

## 📋 Contexto

Brain OS necesita una skill llamada **{nombre_skill}** que:
- **Problema que resuelve**: {resumen del problema en 1-2 oraciones}
- **Categoría**: {sistema / académica / utilidad}
- **Nivel de riesgo**: {🟢 Bajo / 🟡 Medio / 🔴 Alto}
- **Frecuencia de uso**: {diario / semanal / bajo demanda}

---

## 🎯 Capacidades Requeridas

### Capacidad 1: {nombre}
- **Comando**: "{comando natural del usuario}"
- **Input**: {qué recibe}
- **Output**: {qué produce, formato}
- **Ejemplo**: {interacción completa usuario → agente}

### Capacidad 2: {nombre}
[Repetir estructura]

### Capacidad 3: {nombre}
[Repetir estructura]

---

## 🔧 Tareas de Implementación

### FASE 1: Estructura (5 min)
Crear directorio:
skills/{nombre_skill}/
├── SKILL.md
├── scripts/ (si aplica)
│   └── {script_principal}.py
└── references/ (si aplica)

### FASE 2: SKILL.md (30 min)
Implementar documento completo de ≥150 líneas con:

1. **Frontmatter YAML**
name: {nombre_skill}
description: {descripción completa incluyendo triggers}

2. **Cuándo Usar** — Triggers y contextos

3. **Comandos** — Tabla con todos los comandos disponibles

4. **Flujo de Ejecución** — Paso a paso de cada capacidad

5. **Formato de Outputs** — Ejemplos concretos (JSON, tabla, markdown)

6. **Integración** — Con qué otros componentes interactúa

7. **Zonas Protegidas** — Qué NO tocar (si aplica)

8. **Ejemplo de Interacción Completa** — Conversación real

### FASE 3: Scripts (si aplica) (20 min)
{Descripción de scripts necesarios con pseudocódigo}

### FASE 4: Integración (10 min)
1. Agregar en `system-coordinator/SKILL.md` → lista de skills core
2. Agregar en `README.md` → sección Skills Académicas + tabla de comandos

### FASE 5: Testing (10 min)
Ejecutar estos tests:

Test 1: {nombre}
Comando: "{comando}"
Input: {input_específico}
Output esperado: {output_específico}
Criterio: ✅ {medible}

Test 2: {nombre}
[Repetir para ≥5 tests]

### FASE 6: Validación Final
- [ ] SKILL.md tiene frontmatter válido
- [ ] ≥150 líneas de contenido
- [ ] Ejemplos con outputs reales
- [ ] Integrado en system-coordinator
- [ ] Entrada en README.md
- [ ] 5+ tests documentados y pasados

---

## ⚠️ Restricciones
{Lista de restricciones del usuario: zonas protegidas, dependencias, etc.}

## 🚀 COMIENZA IMPLEMENTACIÓN
Procede con FASE 1. Confirma la estructura creada antes de continuar.
```

---

## Template 2: Re-implementación de Skill

Usar después de una auditoría + entrevista de mejora (Modo 3).

```markdown
# 🔄 RE-IMPLEMENTACIÓN: {nombre_skill} v{N+1}

## 📋 Contexto

La skill actual tiene **{score}/100 puntos**. Áreas principales de mejora:

### ✅ QUÉ MANTENER (Funciona Bien)
- {Lista de lo que el usuario confirmó preservar}
- {Comandos actuales que funcionan}
- {Lógica principal operativa}

### 🔧 QUÉ MEJORAR (Brechas Priorizadas por el usuario)
1. 🔴 {Brecha crítica 1} — Impacto: {X}
2. 🔴 {Brecha crítica 2} — Impacto: {X}
3. 🟡 {Brecha media 1} — Impacto: {X}

### ⭐ CAPACIDADES NUEVAS (Si aplica)
- {Capacidad nueva que el usuario pidió}

---

## 🎯 Tareas de Re-implementación

### FASE 0: RESPALDO (OBLIGATORIO)
**CRÍTICO — EJECUTAR PRIMERO**:
1. Crear `skills/{nombre_skill}/backup_v{N}/`
2. Copiar TODO el contenido actual al backup
3. Confirmar que el backup existe y está completo
4. SOLO ENTONCES proceder

### FASE 1: MEJORA DE DOCUMENTACIÓN
Actualizar SKILL.md preservando lo bueno:

**Mantener**: {secciones que funcionan}
**Reescribir**: {secciones con brechas}
**Agregar**: {secciones faltantes: tests, outputs, ejemplos}

Meta: ≥150 líneas, ejemplos con outputs reales

### FASE 2: MEJORA DE CÓDIGO (si aplica)
**Preservar** (no tocar):
- {funciones que funcionan bien}

**Mejorar**:
- Agregar try-catch donde falta
- Mejorar mensajes de error
- Agregar validación de inputs
- Agregar logging (si aplica)

### FASE 3: INTEGRACIÓN
Si no estaba integrada:
1. Agregar en `system-coordinator/SKILL.md`
2. Agregar en `README.md`

### FASE 4: TESTING
Ejecutar los tests nuevos + verificar que lo preservado sigue funcionando.

### FASE 5: COMPARACIÓN
Generar reporte antes/después:

## ANTES (v{N})
- Score: {score_antes}/100
- Brechas críticas: {cantidad}

## DESPUÉS (v{N+1})
- Score: {score_esperado}/100 (+{delta} pts)
- Brechas resueltas: {lista}

## BACKUP
Versión anterior en: skills/{nombre_skill}/backup_v{N}/

---

## 🚀 COMIENZA RE-IMPLEMENTACIÓN
Procede con FASE 0 (Respaldo). Confirma cuando el backup esté creado.
```

---

## Guía de Entrevista: Crear (Modo 1)

### Preguntas Obligatorias (5)

| # | Pregunta | Qué Infiere el Architect |
|:-:|----------|--------------------------|
| 1 | ¿Qué problema resuelve? | Categoría, nombre técnico |
| 2 | Dame 2-3 ejemplos de uso real | Comandos, inputs/outputs |
| 3 | ¿Frecuencia de uso? | Integración con coordinator |
| 4 | ¿Necesita conectarse con algo? | Dependencias, zonas |
| 5 | ¿Algo que NO debería tocar? | Zonas protegidas, rollback |

### Preguntas Opcionales (2)

| # | Pregunta | Cuándo Preguntar |
|:-:|----------|-----------------|
| 6 | Refinamiento contextual | Si hay brechas en las respuestas |
| 7 | ¿Algo más que agregar? | Si el usuario parece tener más ideas |

### Reglas de Entrevista
- Máximo 2 preguntas por mensaje (no abrumar)
- Empezar con P1 sola (es la más abierta)
- P2 y P3 pueden ir juntas
- P4 y P5 pueden ir juntas
- P6-P7 solo si necesario

---

## Guía de Entrevista: Rehacer (Modo 3)

### Preguntas (3 máximo)

| # | Pregunta | Objetivo |
|:-:|----------|----------|
| 1 | ¿Qué funciona bien que debemos MANTENER? | Evitar romper lo bueno |
| 2 | De las brechas, ¿cuáles son MÁS IMPORTANTES? | Priorizar mejoras |
| 3 | ¿Capacidades nuevas o solo mejorar existente? | Definir alcance |

### Reglas
- Si hay auditoría previa, mostrar brechas con números para que el usuario priorice
- Si no hay auditoría previa, ejecutar auditoría rápida primero
- Siempre crear backup ANTES de tocar cualquier archivo
