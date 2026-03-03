---
description: Auditoría periódica de salud de Brain OS. Activa cuando el usuario quiera verificar el estado del sistema, buscar deuda técnica, o hacer mantenimiento preventivo.
---

# 🔍 Workflow de Auditoría — `/brain-os-audit`

Health check del sistema Brain OS. Ejecutar cada 2-4 semanas o cuando algo "se sienta raro".

---

## Secuencia de Auditoría

### Paso 1: Integridad del Sistema
// turbo
1. **Verificar archivos core**:
   ```
   ¿Existen y son legibles?
   - brain_config.md
   - INICIO.md
   - Flujo_Maestro_BrainOS_v2.md
   - CHANGELOG.md
   - config/audit_log.json
   - config/hemingway_bridge.json
   - config/notebooklm_registry.json
   ```

### Paso 2: Skills Health
// turbo
2. **Auditar directorio skills/**:
   ```
   - Contar skills activas vs archivadas
   - Identificar skills sin SKILL.md (directorio vacío o incompleto)
   - Identificar skills con archivos < 100 bytes (posibles fantasmas)
   - Verificar que skills referenciadas en Flujo_Maestro_v2 existen
   ```

### Paso 3: Configuración
// turbo
3. **Validar brain_config.md**:
   ```
   - ¿Hay IDs con caracteres sospechosos (?, ~, `, etc.)?
   - ¿Todos los cursos tienen su mapeo Moodle → Notion → NotebookLM?
   - ¿El esquema BD_TAREAS_MAESTRAS coincide con la realidad en Notion?
   ```

### Paso 4: Workflows
// turbo
4. **Verificar workflows en .agent/workflows/**:
   ```
   - ¿Todos tienen frontmatter YAML con 'description'?
   - ¿Las referencias a archivos/paths son válidas?
   - ¿Los comandos // turbo están usados correctamente?
   ```

### Paso 5: Dashboard
// turbo
5. **Verificar INICIO.md**:
   ```
   - ¿Fecha de "Última sync" tiene más de 3 días?
   - ¿El conteo de skills coincide con la realidad?
   - ¿Todos los comandos listados siguen siendo funcionales?
   - ¿Los estados de NotebookLM son correctos?
   ```

### Paso 6: Higiene del Repositorio
// turbo
6. **Verificar Git y estructura**:
   ```
   - ¿Hay cambios sin commitear? (git status)
   - ¿Hay archivos sueltos en la raíz que deberían estar en tools/?
   - ¿Existe el CHANGELOG.md y tiene entradas recientes?
   - ¿skills/last30days/ tiene acumulación excesiva (>50 archivos)?
   ```

### Paso 7: Integrations Health
7. **Probar conectividad** (si el usuario lo solicita):
   ```
   - Notion MCP: Query simple a BD_TAREAS_MAESTRAS
   - Moodle: Verificar que get_tasks.py ejecuta sin error
   - Pomodoro Timer: python pomodoro_timer.py status
   ```

---

## Reporte de Salud

Al finalizar, generar un reporte con este formato:

```
🔍 AUDITORÍA BRAIN OS — [Fecha]

📊 Score General: [X]/100

✅ Saludable:
   - [lista de componentes OK]

⚠️ Atención:
   - [lista de problemas menores]

🔴 Crítico:
   - [lista de problemas bloqueantes]

📋 Acciones Recomendadas:
   1. [acción prioritaria]
   2. [acción secundaria]
   ...
```

### Cálculo del Score

| Categoría | Peso | Criterio de 100% |
|-----------|------|-------------------|
| Archivos core existen | 20% | Todos legibles y actualizados |
| Skills health | 20% | Sin fantasmas, todas con SKILL.md |
| Config válida | 15% | Sin IDs rotos, mapeos completos |
| Workflows válidos | 15% | Frontmatter YAML correcto |
| Dashboard actualizado | 15% | Sync < 3 días, conteos correctos |
| Git limpio | 15% | Sin cambios pendientes |

---

## Actualización del Audit Log
// turbo
8. **Registrar auditoría**:
   ```
   Actualizar config/audit_log.json con:
   - fecha de auditoría
   - score obtenido
   - problemas encontrados
   - acciones tomadas
   ```

---

## Notas

- Este workflow se activa con "audita Brain OS", "¿cómo está el sistema?", "health check", o `/brain-os-audit`
- No modifica nada por sí solo — solo diagnostica y recomienda
- Las correcciones se aplican con `/brain-os-upgrade` o `/brain-os-dev`
- Recomendación: ejecutar al inicio de cada mes o después de cambios grandes
