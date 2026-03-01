---
name: cleanup-manager
description: Detecta y limpia archivos obsoletos, duplicados y temporales del sistema Brain OS. Usa esta skill cuando el sistema acumule basura, antes de auditorías de system-coordinator, o con los comandos "Escanear basura", "Limpieza rápida", "Limpieza conservadora", "Limpieza profunda".
---

# 🧹 Cleanup Manager

> Mantiene Brain OS limpio y eficiente detectando y eliminando archivos obsoletos de forma segura.

## Cuándo Usar

- Mediante los comandos: `"Escanear basura"`, `"Limpieza rápida"`, etc.
- Automáticamente durante `"Verifica el sistema completo"` (system-coordinator, Sección 6)
- Antes de backups importantes o cambios de semestre
- Cuando el sistema se siente "lento" o desorganizado

---

## Comandos

| Comando | Nivel | Descripción |
|---------|:-----:|-------------|
| "Escanear basura" | 0 | Análisis sin tocar nada — genera reporte |
| "Limpieza rápida" | 1 | Automático, solo lo obvio y 100% seguro |
| "Limpieza conservadora" | 2 | Con confirmación, archiva antes de eliminar |
| "Limpieza profunda" | 3 | Eliminación permanente, requiere confirmación explícita |
| "Restaurar desde archivo" | — | Recuperar archivos del directorio de respaldo |
| "Reporte de limpieza semanal" | — | Estadísticas acumuladas de cleanup_history.json |

---

## Zonas Protegidas 🛡️

Estos directorios **NUNCA** se tocan sin confirmación explícita del usuario:

```
carrera/semestres/2026-1/cursos/   ← Material académico activo
skills/*/SKILL.md                  ← Definiciones de skills
config/                            ← Configuración del sistema
.agent/workflows/                  ← Workflows del sistema
brain_config.md                    ← Configuración central
INICIO.md                         ← Dashboard
README.md                         ← Documentación pública
Flujo_Maestro_BrainOS_v2.md       ← Flujo maestro
tools/pomodoro/config.json         ← Configuración pomodoro
tools/pomodoro/history.json        ← Historial (datos del usuario)
```

> **Regla de oro**: Si un archivo está en una zona protegida, Nivel 1 y 2 lo ignoran. Solo Nivel 3 lo reporta y pide confirmación.

---

## Categorías de Basura Detectadas

### Categoría 1: `__pycache__` — Compilados Python
- **Riesgo**: ⚪ Nulo — se regeneran automáticamente
- **Nivel mínimo**: 1 (auto-limpieza segura)
- **Peso típico**: 7+ MB
- **Ubicación principal**: `skills/notebooklm/.venv/`, `skills/aula-virtual/scripts/`

### Categoría 2: `.old` / `.bak` — Archivos de respaldo obsoletos
- **Riesgo**: ⚪ Nulo si están en browser_state
- **Nivel mínimo**: 1 (para browser_state), 2 (otros)
- **Peso típico**: <1 MB
- **Ubicación principal**: `skills/notebooklm/data/browser_state/`

### Categoría 3: `debug_*` / `temp_*` — Temporales y depuración
- **Riesgo**: 🟡 Bajo — podrían contener contexto útil
- **Nivel mínimo**: 2 (con confirmación)
- **Peso típico**: ~100 KB
- **Ejemplo**: `temp_library_sync.txt`, `debug_course_dump.json`

### Categoría 4: Browser Cache — Datos de Chromium (NotebookLM)
- **Riesgo**: 🟡 Bajo — se regeneran al abrir el navegador
- **Nivel mínimo**: 2 (por volumen alto)
- **Peso típico**: 50+ MB (cache, code cache, model store, GrShaderCache)
- **Ubicación**: `skills/notebooklm/data/browser_state/browser_profile/`

### Categoría 5: Carpetas Vacías
- **Riesgo**: ⚪ Nulo para browser dirs, 🔴 Para carpetas de cursos (estructura intencional)
- **Nivel mínimo**: 1 (solo browser vacíos), NUNCA para `carrera/`
- **Cantidad típica**: ~42 browser + ~42 curso (preservar)

### Categoría 6: Archivos Grandes Huérfanos (>5MB)
- **Riesgo**: 🟡 Variable — requiere análisis individual
- **Nivel mínimo**: 3 (solo con confirmación explícita)
- **Ejemplo**: `node.exe` (81MB) en .venv — necesario para patchright

### Categoría 7: `.log` — Logs del sistema
- **Riesgo**: 🟡 Bajo — contienen info de debug
- **Nivel mínimo**: 2 (con confirmación)
- **Cantidad**: ~13 archivos

---

## Niveles de Limpieza

### Nivel 1: Limpieza Rápida (100% seguro, sin confirmación)

```python
# Acciones automáticas
cleanup_actions = [
    "Eliminar TODOS los __pycache__/ recursivamente",
    "Eliminar .old en browser_state/",
    "Eliminar carpetas vacías en browser_state/ (NO en carrera/)",
    "Eliminar _scan_system.py y _scan_results.txt si existen (temp de esta skill)",
]
```

**Efecto estimado**: ~7-10 MB recuperados, 0 riesgo.

### Nivel 2: Limpieza Conservadora (con confirmación)

Todo lo del Nivel 1, más:
```python
# Listar al usuario para confirmación
confirm_actions = [
    "Archivar debug_* en cleanup_archive/YYYY-MM-DD/",
    "Archivar temp_* en cleanup_archive/YYYY-MM-DD/",
    "Limpiar browser cache (Cache_Data, Code Cache, GrShaderCache)",
    "Archivar .log de browser_state",
    "Archivar tasks.log si tiene más de 30 días",
]
```

**Efecto estimado**: ~50-60 MB recuperados. Archivos movidos a `cleanup_archive/`, no eliminados.

### Nivel 3: Limpieza Profunda (eliminación con confirmación explícita)

Todo lo del Nivel 2 (ejecutado), más:
```python
# Requiere confirmación explícita por CADA elemento
deep_actions = [
    "Eliminar cleanup_archive/ completo (fin del rollback)",
    "Evaluar archivos >5MB individualmente",
    "Evaluar model stores de browser (.tflite con >30 días)",
    "Reportar archivos en zonas protegidas que podrían ser obsoletos",
]
```

**Efecto estimado**: Variable. Puede recuperar 50+ MB adicionales.

---

## Flujo de Ejecución

### "Escanear basura" (Nivel 0)

```
PASO 1 → Ejecutar scripts/cleanup.py --scan
PASO 2 → Generar reporte con categorías y tamaños
PASO 3 → Mostrar recomendaciones por nivel
PASO 4 → NO modificar nada
```

**Formato de reporte:**

```markdown
## 🧹 Escaneo de Basura — [FECHA]

| Categoría | Archivos | Tamaño | Nivel Recomendado |
|-----------|:--------:|:------:|:-----------------:|
| __pycache__ | XX | XX MB | 1 (auto) |
| .old browser | XX | XX KB | 1 (auto) |
| debug_/temp_ | XX | XX KB | 2 (confirmar) |
| Browser cache | XX | XX MB | 2 (confirmar) |
| Dirs vacíos (no-curso) | XX | 0 | 1 (auto) |
| .log | XX | XX KB | 2 (confirmar) |
| **TOTAL recuperable** | **XX** | **XX MB** | — |

💡 Ejecuta "Limpieza rápida" para limpiar Nivel 1 automáticamente.
```

### "Limpieza rápida" / "Limpieza conservadora" / "Limpieza profunda"

```
PASO 1 → Ejecutar escaneo (igual que Nivel 0)
PASO 2 → Filtrar acciones según nivel
PASO 3 → [N2/N3] Mostrar lista de archivos y pedir confirmación
PASO 4 → Ejecutar acciones aprobadas
PASO 5 → Registrar en cleanup_history.json
PASO 6 → Generar reporte post-limpieza
```

---

## Rollback y Seguridad

### Directorio de Archivo
```
cleanup_archive/
├── 2026-02-12/
│   ├── debug_course_dump.json
│   ├── temp_library_sync.txt
│   └── manifest.json      ← Lista de archivos + rutas originales
└── 2026-02-15/
    └── ...
```

### manifest.json
```json
{
  "date": "2026-02-12T23:47:00",
  "level": 2,
  "files": [
    {
      "original_path": "skills/aula-virtual/scripts/debug_course_dump.json",
      "archived_as": "debug_course_dump.json",
      "size_kb": 25,
      "category": "debug"
    }
  ]
}
```

### "Restaurar desde archivo"
```
PASO 1 → Leer cleanup_archive/ → Listar sesiones disponibles
PASO 2 → Usuario selecciona sesión o archivo específico
PASO 3 → Copiar archivo de vuelta a ruta original
PASO 4 → Registrar restauración en cleanup_history.json
```

---

## Historial de Limpieza

### cleanup_history.json
```json
{
  "last_scan": "2026-02-12T23:47:00",
  "last_cleanup": null,
  "total_recovered_mb": 0,
  "sessions": []
}
```

### Sesión de limpieza registrada
```json
{
  "date": "2026-02-12T23:47:00",
  "level": 1,
  "files_removed": 64,
  "space_recovered_mb": 7.2,
  "categories": {
    "__pycache__": {"files": 60, "mb": 7.0},
    ".old": {"files": 28, "mb": 0.1},
    "empty_dirs": {"files": 42, "mb": 0}
  },
  "errors": []
}
```

---

## Integración con System Coordinator

### En "Verifica el sistema completo" — Sección 6: Higiene

```markdown
## 6. Higiene del Sistema 🧹

| Métrica | Valor | Estado |
|---------|:-----:|:------:|
| __pycache__ | XX dirs (XX MB) | 🟢/🟡/🔴 |
| Archivos temporales | XX | 🟢/🟡/🔴 |
| Browser cache | XX MB | 🟢/🟡/🔴 |
| Última limpieza | FECHA | 🟢/🟡/🔴 |
| Espacio recuperable | XX MB | — |

Criterios:
  < 10MB basura → 🟢
  10-50MB       → 🟡 Recomendar "Limpieza rápida"
  > 50MB        → 🔴 Recomendar "Limpieza conservadora"
```

### En "Auditoría de uso semanal"
```
- Espacio recuperado esta semana: XX MB
- Limpiezas ejecutadas: X
- Archivos en cleanup_archive/: X (XX MB pendiente de purga)
```

---

## Archivos de la Skill

```
skills/cleanup-manager/
├── SKILL.md                         ← Este archivo
├── scripts/
│   ├── cleanup.py                   ← Script principal de escaneo y limpieza
│   └── cleanup_config.json          ← Reglas y zonas protegidas
└── (generados en runtime)
    cleanup_archive/                 ← Archivos archivados (rollback)
    cleanup_history.json             ← Historial de operaciones
```

---

## Notas

- El agente puede ejecutar el script o hacer la limpieza manualmente siguiendo los pasos
- `cleanup.py --scan` solo reporta, `--clean --level N` ejecuta la limpieza
- Los `.venv/` son respetados porque contienen dependencias instaladas (solo se limpian sus `__pycache__`)
- Las carpetas vacías de `carrera/` son **intencionales** (estructura de cursos) — NUNCA eliminar
- Browser state de NotebookLM se regenera al reabrir el navegador automatizado

---

## 🧪 Escenarios de Prueba

### Test 1: Escaneo en sistema limpio

```
Input:    "Escanear basura" (después de limpieza reciente)
Espera:   Reporte con todas las categorías en 0 o mínimo
Verifica: Tabla con ≤5 MB recuperables, ningún 🔴
Output:   "Sistema limpio. No se recomienda limpieza."
```

### Test 2: Detección de `__pycache__`

```
Input:    Proyecto con 60+ dirs __pycache__ (~7 MB)
Espera:   Categoría 1 reporta correctamente archivos y tamaño
Verifica: Conteo coincide con `find . -name "__pycache__" | wc -l`
Output:   "Encontrados XX __pycache__ (XX MB) → Nivel 1 recomendado"
```

### Test 3: Nivel 1 respeta zonas protegidas

```
Input:    "Limpieza rápida" con __pycache__ dentro de carrera/ y fuera
Espera:   Elimina __pycache__ de skills/ pero NO toca carrera/
Verifica: carrera/ intacto, __pycache__ de skills/ eliminados
Output:   Reporte post-limpieza muestra solo archivos fuera de zonas protegidas
```

### Test 4: Nivel 2 archiva correctamente

```
Input:    "Limpieza conservadora" con debug_test.json y temp_sync.txt
Espera:   Crea cleanup_archive/YYYY-MM-DD/ con manifest.json
Verifica: - Archivos originales ya no existen en ruta original
          - cleanup_archive/ contiene archivos + manifest
          - manifest.json tiene rutas originales correctas
Output:   "Archivados 2 archivos en cleanup_archive/2026-02-26/"
```

### Test 5: Restauración desde archivo

```
Input:    "Restaurar desde archivo" → selecciona debug_test.json
Espera:   Copia archivo desde cleanup_archive/ a ruta original
Verifica: - Archivo existe nuevamente en ruta original
          - cleanup_history.json registra la restauración
Output:   "Restaurado debug_test.json → skills/aula-virtual/scripts/"
```

### Test 6: Nivel 3 pide confirmación individual

```
Input:    "Limpieza profunda" con node.exe (81MB) y .tflite (15MB)
Espera:   Lista cada archivo >5MB individualmente para aprobación
Verifica: - NO elimina sin confirmación explícita por archivo
          - Si usuario rechaza node.exe, solo elimina .tflite
Output:   "¿Eliminar node.exe (81 MB)? [sí/no]" por cada archivo
```
