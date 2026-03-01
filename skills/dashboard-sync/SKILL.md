---
name: dashboard-sync
description: Sincroniza automáticamente el archivo INICIO.md (panel de control de Brain OS) con la información actual del sistema. Usar cuando el usuario diga "Actualiza el dashboard", "Sincroniza INICIO.md", "Actualiza el panel de control", después de agregar notebooks a NotebookLM, o después de implementar nuevas funcionalidades.
---

# 📊 Dashboard Sync

> Mantiene `INICIO.md` sincronizado con el estado real de Brain OS.

## Cuándo Usar

- Después de agregar notebooks a NotebookLM
- Después de implementar nuevas integraciones
- Cuando el usuario pida "Actualiza el dashboard"
- Al inicio de cada semestre o aporte
- Automáticamente durante el workflow "Buenos Días"

---

## Comandos

| Comando | Función |
|---------|---------|
| "Actualiza el dashboard" | Sync completo de todas las secciones |
| "Sincroniza INICIO.md" | Alias del anterior |
| "Preview del dashboard" | Muestra cambios sin aplicar |
| "Actualiza la sección [X]" | Sync parcial de una sección específica |

---

## Secciones de INICIO.md

| # | Sección | Fuente de Datos | Frecuencia |
|:-:|---------|-----------------|:----------:|
| 1 | 📊 Estado Actual | `brain_config.md` + sistema | Cada sync |
| 2 | 🛠️ Skills Disponibles | `skills/` directory scan | Al agregar/eliminar skills |
| 3 | 🔬 NotebookLM | `brain_config.md` → notebooks | Al agregar notebooks |
| 4 | 📅 Próximas Tareas | Notion `BD_TAREAS_MAESTRAS` | Diario (Buenos Días) |
| 5 | 🌉 Hemingway Bridge | `config/hemingway_bridge.json` | Cierre diario |
| 6 | 🐻 Cronobiología | `brain_config.md` | Rara vez (cambio de hábitos) |

---

## Flujo de Sincronización

```
PASO 1 → Leer fuentes
   brain_config.md       → cursos, notebooks, cronobiología
   skills/ directory     → conteo y categorización
   Notion BD_TAREAS      → tareas pendientes (si disponible)
   hemingway_bridge.json → último hilo de trabajo

PASO 2 → Generar contenido actualizado
   Para cada sección:
   - Leer template de references/sections.md
   - Rellenar con datos actuales
   - Comparar con INICIO.md actual

PASO 3 → Aplicar cambios
   - Identificar secciones desactualizadas
   - Reemplazar solo las secciones que cambiaron
   - Preservar contenido custom del usuario (marcado con <!-- custom -->)
   - Actualizar timestamp de última sincronización

PASO 4 → Confirmar
   - Mostrar resumen de cambios
   - Actualizar last_sync en config/sync_status.json
```

---

## Formato de Cada Sección

### 📊 Estado Actual

```markdown
## 📊 ESTADO ACTUAL

| Métrica | Valor |
|---------|-------|
| 📅 Semestre | 2026-1 |
| 📝 Aporte | Primero |
| 🛠️ Skills activas | 29 |
| 🔬 Notebooks | 5 conectados |
| 🍅 Pomodoros hoy | X sesiones |
| 🧹 Última limpieza | YYYY-MM-DD |
| ⏰ Última sync | YYYY-MM-DD HH:MM |
```

### 🛠️ Skills Disponibles

```markdown
## 🛠️ SKILLS DISPONIBLES (29)

| Categoría | Skills |
|-----------|--------|
| 🎓 Académicas | `aula-virtual` `notebooklm` `pomodoro` `library-manager` |
| ⚙️ Sistema | `system-coordinator` `dashboard-sync` `cleanup-manager` `elite-skill-architect` `architecture` |
| 📋 Planificación | `planning` `planning-with-files` `executing-plans` |
| ✍️ Escritura | `brainstorming` `doc-coauthoring` `copywriting` `copy-editing` `content-creator` |
| 🔍 Investigación | `research-engineer` `prompt-engineer` |
| 📄 Documentos | `pdf` `docx-official` `pptx-official` `xlsx-official` |
```

### 🔬 NotebookLM

```markdown
### 🔬 NotebookLM (Conectados: X ✅)

| Curso | Comando |
|-------|---------|
| 📗 Economía Ambiental | "Consulta mi libro de Economía Ambiental: [pregunta]" |
| 📘 Economía Internacional I | "Consulta mi libro de Economía Internacional: [pregunta]" |
```

### 🌉 Hemingway Bridge

```markdown
### 🌉 Hemingway Bridge
> **Último hilo**: [contenido de hemingway_bridge.json]
> **Fecha**: YYYY-MM-DD HH:MM
```

---

## Ejemplo: Antes vs Después

### Antes (desactualizado)
```
🛠️ SKILLS DISPONIBLES (32)
| ⚙️ Sistema | `dashboard-sync` `skill-creator` |
```

### Después (sincronizado)
```
🛠️ SKILLS DISPONIBLES (29)
| ⚙️ Sistema | `system-coordinator` `dashboard-sync` `cleanup-manager` `elite-skill-architect` `architecture` |
```

---

## Manejo de Errores

| Error | Causa | Solución |
|-------|-------|----------|
| Notion no disponible | Sin conexión o token expirado | Sync parcial: omitir sección de tareas, marcar como "offline" |
| INICIO.md no existe | Archivo eliminado accidentalmente | Regenerar desde template completo |
| brain_config.md vacío | Configuración perdida | Notificar al usuario, no sobrescribir INICIO.md |
| Sección no encontrada | INICIO.md modificado manualmente | Buscar por headers, agregar sección si falta |
| hemingway_bridge.json vacío | No se hizo cierre diario | Mostrar "No hay hilo activo" |

---

## Archivos de la Skill

```
skills/dashboard-sync/
├── SKILL.md                      ← Este archivo
├── references/
│   └── sections.md               ← Templates detallados de cada sección
└── scripts/
    └── sync_dashboard.py         ← Script de sync automático (opcional)
```

---

## 🧪 Escenarios de Prueba

### Test 1: Sync completo exitoso

```
Input:    "Actualiza el dashboard"
Espera:   INICIO.md actualizado con datos actuales
Verifica: - Conteo de skills coincide con `ls skills/`
          - Timestamp de última sync actualizado
          - Secciones con datos reales (no placeholders)
Output:   "Dashboard actualizado: 4 secciones modificadas"
```

### Test 2: Sync con Notion offline

```
Input:    "Actualiza el dashboard" (sin conexión a Notion)
Espera:   Sync parcial — actualiza todo excepto tareas
Verifica: - Sección de tareas muestra "⚠️ Sin conexión"
          - Resto de secciones actualizadas correctamente
Output:   "Dashboard actualizado (parcial). Notion: offline"
```

### Test 3: Sync de sección específica

```
Input:    "Actualiza la sección de Skills"
Espera:   Solo modifica la sección 🛠️ Skills
Verifica: - Solo esa sección cambió
          - Conteo correcto
Output:   "Sección Skills actualizada: 29 skills"
```

### Test 4: Preview sin modificar

```
Input:    "Preview del dashboard"
Espera:   Muestra cambios que se harían, sin tocar INICIO.md
Verifica: INICIO.md NO modificado (comparar timestamps)
Output:   Diff con cambios propuestos
```
