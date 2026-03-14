---
name: architecture
description: Asistente de Arquitectura Activo para Brain OS. Genera registros de decisión (ADRs), analiza estructuras de código, sugiere patrones de diseño y mantiene la integridad arquitectónica del sistema. Usar para "Tomar una decisión técnica", "Crear un ADR", "Analizar estructura", "Consultar patrones" o "Diseñar una nueva feature".
allowed-tools: Read, Glob, Grep, RunCommand
trigger_conditions:
  - "Tomar una decisión técnica"
  - "Crear un ADR para [decisión]"
  - "Analizar estructura del código"
  - "Consultar patrones de diseño para [X]"
  - "Diseñar arquitectura de [feature]"
usage_constraints: "Solo para decisiones arquitectónicas y análisis estructural. No usar para implementación de código (usar executing-plans) ni para planificación de tareas (usar planning)."
category: "Planificación"
parameters:
  action: "Operación: adr | analyze | patterns | design"
  subject: "Tema o componente a analizar (string)"
---

# 🏗️ Architecture Decision Assistant (Elite Tier)

> "Architecture is about the important stuff. Whatever that is." — Ralph Johnson

## 🌟 Capacidades Principales

| Modo | Trigger | Qué Hace |
|------|---------|----------|
| 📝 **Decidir** | "Toma una decisión sobre [tema]" | Guía el proceso de decisión y **genera un ADR** numerado. |
| 🔍 **Analizar** | "Analiza la estructura de [path]" | Escanea código/carpetas y sugiere mejoras basadas en patrones. |
| 🧠 **Consultar** | "¿Qué patrón uso para X?" | Busca en la base de conocimiento y recomienda soluciones. |
| 📐 **Diseñar** | "Diseña la funcionalidad [X]" | Crea un plan técnico preliminar (diagramas + componentes). |

## 🚀 Comandos

### Gestión de ADRs (Architecture Decision Records)

```bash
# Crear un nuevo ADR interactivo
"Crea un ADR sobre el uso de Supabase"
"Registra una decisión de arquitectura"

# Listar decisiones existentes
"Lista los ADRs"
"¿Qué decidimos sobre la base de datos?"
```

### Análisis y Calidad

```bash
# Analizar estructura actual
"Analiza la skill [nombre]"
"Revisa la arquitectura de [carpeta]"

# Consultar patrones
"Patrones para manejo de errores"
"Mejores prácticas para APIs"
```

---

## 📝 Workflow de Decisiones (ADR)

El asistente sigue el estándar [MADR](https://adr.github.io/madr/) para registrar decisiones importantes.

**Flujo:**
1.  **Contexto**: ¿Cuál es el problema y las restricciones?
2.  **Opciones**: ¿Qué alternativas estamos considerando?
3.  **Drivers**: ¿Qué fuerzas influyen (performance, costo, tiempo)?
4.  **Decisión**: ¿Qué elegimos y por qué?
5.  **Generación**: Se crea el archivo `docs/adrs/NNN-titulo-kebab-case.md`.

**Ubicación de ADRs:**
Todos los registros se guardan en: `docs/adrs/`

---

## 🛠️ Herramientas Internas

La skill utiliza scripts en `skills/architecture/scripts/` para automatizar tareas:

1.  **`adr_generator.py`**:
    *   Genera el archivo Markdown con el siguiente número disponible.
    *   Usa el template en `skills/architecture/templates/adr-template.md`.

2.  **`file_analyzer.py`**:
    *   Recorre un directorio y genera un árbol visual.
    *   Puede contar líneas, detectar tipos de archivos y sugerir refactorizaciones simples.

---

## 🔗 Integración con Brain OS

Esta skill es parte del **Núcleo Técnico** y colabora con:
*   `system-coordinator`: Para validar que las decisiones no rompan la integridad del sistema.
*   `elite-skill-architect`: Para asegurar que las nuevas skills sigan los patrones definidos.

### Reglas de Oro
1.  **Simplicidad Primero**: No sobre-diseñar. Elegir la solución más simple que funcione.
2.  **Documentar Siempre**: Si se discute > 5 min, merece un ADR.
3.  **Consistencia**: Seguir las convenciones de nombres y estructuras existentes.

---

## 📂 Estructura de la Skill

```
skills/architecture/
├── SKILL.md                 ← Este archivo
├── scripts/
│   ├── adr_generator.py     ← Generador de ADRs
│   └── file_analyzer.py     ← Analizador de estructura
├── templates/
│   └── adr-template.md      ← Plantilla MADR
└── backup_v1/               ← Versión anterior (solo lectura)
```
