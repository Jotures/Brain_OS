---
name: planning
description: Planificación estructurada de tareas con desglose atómico, criterios de verificación, y compatibilidad con Brain OS. Usar cuando el usuario pida un plan, quiera implementar una feature, refactorizar código, o iniciar un trabajo multi-paso. Se activa con "Planifica [X]", "Haz un plan para [X]", "Necesito un plan", o antes de cualquier tarea compleja.
trigger_conditions:
  - "Planifica [X]"
  - "Haz un plan para [X]"
  - "Necesito un plan"
  - "Tarea multi-paso compleja (>3 pasos)"
  - "Implementar feature nueva"
  - "Refactorizar código o estructura"
usage_constraints: "No usar para tareas simples de un solo paso. No usar para investigación pura (usar research-engineer). No genera código directamente, solo el plan estructurado."
category: "Planificación"
parameters:
  task: "Descripción de la tarea a planificar (string)"
  granularity: "Nivel de detalle: high-level | detailed | atomic (default: detailed)"
---

# 📋 Planning

> Convierte solicitudes complejas en planes accionables con pasos atómicos y verificación clara.

## Cuándo Usar

- Antes de cualquier tarea multi-paso (>3 pasos)
- Implementar features nuevas
- Refactorizar código o estructura
- Resolver bugs complejos
- Cuando el usuario dice "Planifica", "Plan para", "Necesito organizar"

## Principios Fundamentales

### 1. Mantenerlo CORTO
| ❌ Mal | ✅ Bien |
|--------|---------|
| 50 tareas con sub-sub-tareas | 5-10 tareas claras máximo |
| Cada micro-paso listado | Solo items accionables |
| Descripciones verbosas | Una línea por tarea |

> **Regla**: Si el plan ocupa más de 1 página, simplificar.

### 2. Ser ESPECÍFICO
| ❌ Mal | ✅ Bien |
|--------|---------|
| "Configurar el proyecto" | "Ejecutar `npm init -y`" |
| "Agregar autenticación" | "Crear `auth.py` con login por token" |
| "Arreglar los estilos" | "Modificar `styles.css:L42` → cambiar `display: flex`" |

### 3. Cada Tarea es VERIFICABLE
Cada paso debe tener un criterio de "¿cómo sé que terminé?".

### 4. Granularidad Bite-Sized
Cada paso toma **2-5 minutos**:
- "Escribir el test" → un paso
- "Ejecutar el test y verificar que falla" → un paso
- "Implementar la función" → un paso
- "Ejecutar tests y verificar que pasan" → un paso

## Estructura del Plan

```markdown
# [Nombre de la Tarea]

## Objetivo
Una oración: ¿Qué estamos construyendo/arreglando?

## Alcance
- **Incluye**: [qué sí cubrimos]
- **Excluye**: [qué no cubrimos]

## Tareas
- [ ] Tarea 1: [Acción específica] → Verificar: [Cómo comprobar]
- [ ] Tarea 2: [Acción específica] → Verificar: [Cómo comprobar]
- [ ] Tarea 3: [Acción específica] → Verificar: [Cómo comprobar]
...

## Hecho Cuando
- [ ] [Criterio principal de éxito]

## Preguntas Abiertas
- [Máximo 3 preguntas si las hay]
```

> **Eso es todo.** Sin fases, sin sub-secciones, a menos que sea realmente necesario.

## Flujo de Trabajo

```
PASO 1 → Contexto
  Leer README.md, documentación, y archivos relevantes del proyecto
  Identificar restricciones (lenguaje, frameworks, tests existentes)

PASO 2 → Interacción Mínima
  Preguntar MÁXIMO 1-2 preguntas y solo si son bloqueantes
  Hacer supuestos razonables para lo que no es bloqueante

PASO 3 → Generar Plan
  Usar la estructura de arriba
  Máximo 10 tareas (si necesita más → dividir en planes separados)
  Cada tarea empieza con verbo: "Crear...", "Modificar...", "Verificar..."

PASO 4 → Ejecutar o Entregar
  Opción A: Ejecutar el plan directamente (ver `executing-plans`)
  Opción B: Guardar el plan como archivo para ejecución posterior
```

## Variantes por Tipo de Proyecto

| Tipo | Enfoque |
|------|---------|
| **Proyecto nuevo** | Stack → MVP → estructura de archivos |
| **Feature nueva** | Archivos afectados → dependencias → verificación |
| **Bug fix** | Root cause → archivo/línea → test del fix |
| **Refactor** | Impacto → cambios → regression tests |

## Integración con Brain OS

- Los planes para tareas académicas pueden referir a `aula-virtual` para deadlines
- Para tareas de Notion, consultar `BD_TAREAS_MAESTRAS` antes de planificar
- Si el plan es complejo (>5 tareas), considerar usar `planning-with-files` en su lugar
- Si el plan requiere diseño previo, usar `brainstorming` primero

## Skills Complementarias

| Necesitas... | Usa... |
|-------------|--------|
| Planificación persistente en disco | `planning-with-files` |
| Ejecutar un plan paso a paso | `executing-plans` |
| Diseño antes de planificar | `brainstorming` |
| Plan para crear una skill | `elite-skill-architect` |

## Ejemplo de Interacción

```
Usuario: "Planifica cómo agregar un sistema de recordatorios"

Agente genera:

# Sistema de Recordatorios

## Objetivo
Crear un sistema de recordatorios que notifique tareas próximas de BD_TAREAS.

## Alcance
- Incluye: Lectura de Notion, generación de alertas, integración con Buenos Días
- Excluye: Notificaciones push nativas, app móvil

## Tareas
- [ ] 1. Consultar BD_TAREAS → filtrar por fecha_limite < 3 días → Verificar: JSON con tareas
- [ ] 2. Crear función format_reminders() → Verificar: output en formato markdown
- [ ] 3. Integrar en workflow buenos-dias.md → Verificar: "Buenos días" muestra recordatorios
- [ ] 4. Agregar manejo de errores (Notion offline) → Verificar: funciona sin conexión
- [ ] 5. Documentar en INICIO.md → Verificar: sección visible en dashboard

## Hecho Cuando
- [ ] "Buenos días" muestra recordatorios de tareas próximas
```

## Notas

- **No copiar plantillas genéricas** — cada plan es único
- **Actualizar progreso** — marcar `[x]` al completar cada tarea
- Si los pasos exceden 10, dividir en múltiples planes
- Planes para Brain OS deben guardar archivos en la estructura existente del proyecto
