---
description: Workflow para mejorar, refactorizar o corregir componentes existentes de Brain OS. Activa cuando el usuario quiera mejorar skills, arreglar workflows, o hacer refactoring.
---

# 🔄 Workflow de Mejora — `/brain-os-upgrade`

Protocolo para modificar componentes existentes de Brain OS sin introducir regresiones.

---

## Regla de Oro

> **Commit antes de tocar.** Nunca refactorizar sin tener el estado actual guardado en Git.

---

## Fases de Mejora

### Fase 1: Lectura Completa
// turbo
1. **Leer el archivo completo** que se va a mejorar — no asumir su contenido:
   ```
   - Leer el archivo target de principio a fin
   - Identificar: funciones, dependencias, IDs hardcodeados, imports
   - Buscar referencias cruzadas en Flujo_Maestro_BrainOS_v2.md e INICIO.md
   ```

### Fase 2: Análisis Crítico
2. **Diagnosticar problemas** — Responder estas preguntas:
   ```
   ¿Qué falla? (bugs, errores silenciosos)
   ¿Qué es redundante? (código duplicado, skills que se solapan)
   ¿Qué viola DRY? (lógica copiada entre archivos)
   ¿Qué está desactualizado? (IDs viejos, paths rotos, referencias muertas)
   ¿Qué falta? (error handling, type hints, documentación)
   ```

### Fase 3: Propuesta Diff
3. **Mostrar al usuario exactamente qué cambiará** — formato diff:
   ```
   Presentar:
   - Qué líneas se modifican (antes/después)
   - Qué archivos secundarios se actualizan
   - Qué riesgos tiene el cambio
   ```
   **⚠️ NO APLICAR sin aprobación del usuario.**

### Fase 4: Aplicación Quirúrgica
4. **Aplicar cambios mínimos** — no reemplazar archivos enteros:
   ```
   - Usar ediciones puntuales, no sobrescribir
   - Mantener comentarios existentes relevantes
   - No cambiar formato/estilo sin razón funcional
   ```

### Fase 5: Verificación de Regresión
// turbo
5. **Verificar que el resto del sistema no se rompió**:
   ```
   Si el archivo es referenciado en Flujo_Maestro_BrainOS_v2.md → verificar coherencia
   Si el archivo es referenciado en INICIO.md → verificar que los comandos siguen
   Si el archivo usa IDs de brain_config.md → verificar que los IDs sean correctos
   Si es un script Python → ejecutar para verificar que no hay SyntaxError
   ```

### Fase 6: Documentación y Cierre
// turbo
6. **Actualizar referencias**:
   ```
   - INICIO.md → Si cambió un comando o nombre de skill
   - brain_config.md → Si se corrigieron IDs
   - Flujo_Maestro_BrainOS_v2.md → Si cambió un flujo operativo
   ```

// turbo
7. **Registrar el cambio** (AUTO-DOCUMENTACIÓN):
   ```
   a) CHANGELOG.md → Agregar línea con formato:
      - `{tipo}` — {descripción breve}
      Tipos válidos: refactor | fix | docs | cleanup
   
   b) config/dev_registry.json → Agregar nueva entrada al array "entries":
      {
        "id": "{siguiente_número}",
        "date": "{YYYY-MM-DD}",
        "type": "{refactor|fix|docs|cleanup}",
        "description": "{descripción del cambio}",
        "files_affected": ["{lista de archivos modificados}"],
        "workflow_used": "/brain-os-upgrade"
      }
   ```

8. **Commit**:
   ```powershell
   git add .
   git commit -m "refactor: [descripción breve]"
   # o: git commit -m "fix: [descripción del bug corregido]"
   ```

---

## Tipos de Mejora

| Tipo | Ejemplo | Riesgo |
|------|---------|--------|
| **Corrección** | Fix de un path roto en un script | 🟢 Bajo |
| **Actualización** | Cambiar IDs obsoletos | 🟡 Medio |
| **Refactoring** | Reorganizar la lógica de una skill | 🟠 Medio-Alto |
| **Migración** | Mover archivos de ubicación | 🔴 Alto |

---

## Notas

- Este workflow se activa con "mejora X", "arregla Y", "refactoriza Z", o `/brain-os-upgrade`
- Si se descubre que el componente debe reconstruirse desde cero → cambiar a `/brain-os-dev`
- Para cambios masivos que afectan múltiples archivos, considerar crear un branch de Git primero
