# 🎭 Playwright Skill — Contexto Brain OS

## Uso Actual de Browser Automation en Brain OS

| Integración | Scripts | Estado |
|-------------|---------|--------|
| Aula Virtual (Moodle) | `skills/aula-virtual/scripts/download_files.py` | ✅ Activo |
| NotebookLM | `skills/notebooklm/` | ⚠️ Frágil (UI cambia frecuentemente) |

## Selectores Conocidos

### Moodle (Aula Virtual UAndina)
- Login: depende de la instancia institucional
- Cursos: mapeo en `brain_config.md` → `AULA_VIRTUAL_*`
- Archivos: `skills/aula-virtual/scripts/course_map.py`

### NotebookLM
> ⚠️ Los selectores de NotebookLM son **inestables**. Google actualiza la UI frecuentemente.

Ver conversación `cc41bc12` (Fixing NotebookLM Upload) para el último estado de los selectores.

## Buenas Prácticas para Brain OS

1. **Siempre usar `wait_for_selector`** con timeout explícito (5-10s)
2. **Screenshots en error**: Capturar screenshot cuando un selector falla para debugging visual
3. **Fallback manual**: Si Playwright falla, dar al usuario la URL + instrucciones para hacer la acción manualmente
4. **No guardar credenciales en código**: Usar variables de entorno o archivos `.env` ignorados por git

## Integración con Otras Skills

- `systematic-debugging` → cuando un selector deja de funcionar
- `aula-virtual` → es el consumidor principal de Playwright
- `notebooklm` → segundo consumidor, más frágil
- `mcp-builder` → alternativa futura: reemplazar browser automation con API directa donde sea posible
