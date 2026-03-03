---
description: Workflow para agregar features, skills, scripts o integraciones nuevas a Brain OS. Activa cuando el usuario quiera construir algo nuevo en el sistema.
---

# 🔧 Workflow de Desarrollo — `/brain-os-dev`

Protocolo estructurado para evolucionar Brain OS sin romper lo que funciona.

---

## Pre-requisito: Carga de Contexto

// turbo
1. **Cargar arquitectura** — Leer estos archivos antes de proponer nada:
   ```
   Obligatorios:
   - brain_config.md          → IDs, esquemas, mapeos
   - INICIO.md                → Estado actual del sistema
   - Flujo_Maestro_BrainOS_v2.md → Flujo operativo completo
   
   Si aplica al cambio:
   - skills/[skill-relevante]/SKILL.md
   - .agent/workflows/brain-os-study.md
   ```

---

## Fases de Desarrollo

### Fase 1: Diagnóstico (¿Ya existe?)
// turbo
2. **Buscar duplicados** — Antes de crear algo nuevo:
   ```
   Buscar en skills/ → ¿Existe una skill similar?
   Buscar en tools/ → ¿Existe un script que haga esto?
   Buscar en .agent/workflows/ → ¿Ya hay un workflow para esto?
   ```
   Si ya existe algo parcial → considerar `/brain-os-upgrade` en lugar de crear desde cero.

### Fase 2: Diseño
3. **Proponer arquitectura** al usuario:
   ```
   Definir:
   - Tipo: skill | script | workflow | config | integración
   - Ubicación exacta del archivo
   - Dependencias con otros componentes
   - IDs de Notion/MCP necesarios (si aplica)
   ```
   **⚠️ NO CONTINUAR sin aprobación del usuario.**

### Fase 3: Implementación
4. **Construir** siguiendo los estándares Brain OS:
   ```
   - DRY: No repetir lógica que ya existe en otra skill/script
   - IDs desde brain_config.md: Nunca hardcodear IDs de Notion
   - Comentarios "por qué": Explicar decisiones de diseño, no sintaxis
   - Type hints: Obligatorios en Python (PEP 484)
   - Error handling: try/except en toda llamada externa (API, MCP, filesystem)
   - Secrets: Usar os.getenv(), nunca embeber keys
   ```

### Fase 4: Integración
// turbo
5. **Conectar con el sistema**:
   ```
   Si requiere IDs → Agregar a brain_config.md
   Si es skill → Verificar SKILL.md con frontmatter name/description
   Si es workflow → Verificar frontmatter YAML con description
   Si afecta el flujo diario → Actualizar Flujo_Maestro_BrainOS_v2.md
   ```

### Fase 5: Verificación
6. **Probar en aislamiento** antes de integrar al flujo principal:
   ```
   Scripts Python: Ejecutar con datos de prueba
   Skills: Simular invocación con "Usa la skill X para Y"
   Workflows: Verificar que el frontmatter es válido
   Integraciones MCP: Hacer una query de prueba
   ```

### Fase 6: Documentación y Cierre
// turbo
7. **Actualizar documentación**:
   ```
   - INICIO.md → Agregar nuevo comando/skill si aplica
   - brain_config.md → Si se agregaron IDs nuevos
   ```

// turbo
8. **Registrar el cambio** (AUTO-DOCUMENTACIÓN):
   ```
   a) CHANGELOG.md → Agregar línea con formato:
      - `{tipo}` — {descripción breve}
      Bajo la fecha actual. Si la fecha no existe, crear nuevo bloque:
      ## {YYYY-MM-DD}
   
   b) config/dev_registry.json → Agregar nueva entrada al array "entries":
      {
        "id": "{siguiente_número}",
        "date": "{YYYY-MM-DD}",
        "type": "{feat|refactor|fix|docs|cleanup}",
        "description": "{descripción del cambio}",
        "files_affected": ["{lista de archivos creados/modificados}"],
        "workflow_used": "/brain-os-dev"
      }
   ```

9. **Commit**:
   ```powershell
   git add .
   git commit -m "feat: [descripción breve del cambio]"
   ```

---

## Checklist de Calidad (pre-commit)

- [ ] ¿El código sigue DRY? (no duplica lógica existente)
- [ ] ¿Los IDs vienen de `brain_config.md`?
- [ ] ¿Se actualizó `INICIO.md`?
- [ ] ¿Se agregó entrada en `CHANGELOG.md`?
- [ ] ¿Se verificó que no rompe workflows existentes?
- [ ] ¿El usuario aprobó el diseño antes de implementar?

---

## Notas

- Este workflow se activa cuando el usuario dice "quiero agregar X", "crea una nueva skill", "integra Y", o usa `/brain-os-dev`
- Si el cambio es una mejora de algo existente, usar `/brain-os-upgrade` en su lugar
- Priorizar siempre la extensión sobre la reescritura
