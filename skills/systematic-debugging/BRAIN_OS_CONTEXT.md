# 🔍 Systematic Debugging — Contexto Brain OS

## Protocolo de Debugging para Brain OS

Cuando un script o flujo del sistema falla, seguir este orden:

### Paso 1: Identificar el Síntoma
- ¿Qué comando falló? (boot, sync, pomodoro, cleanup)
- ¿Cuál es el mensaje de error?
- ¿Cuándo ocurrió por última vez correctamente?

### Paso 2: Verificar Integridad del Sistema
```
Ejecutar: "Verifica el sistema" → system-coordinator
```
Esto chequea:
- IDs de Notion accesibles
- Notebooks de NotebookLM respondiendo
- Estructura de carpetas intacta

### Paso 3: Revisar Logs
| Log | Ubicación | Qué contiene |
|-----|-----------|--------------|
| Cleanup | `_cleanup_test_output.txt` | Último run de limpieza |
| Pomodoro | `tools/pomodoro/history.json` | Sesiones recientes |
| Aula Virtual | `skills/aula-virtual/scripts/*.log` | Errores de sync |

### Paso 4: Reproducir en Aislamiento
Ejecutar solo la skill/script que falló, no el flujo completo:
```python
# En vez del boot completo, probar solo el paso que falla
python skills/aula-virtual/scripts/download_files.py
```

### Paso 5: Fix & Verify
1. Aplicar fix mínimo
2. Correr `system-coordinator` para verificar
3. Re-ejecutar el flujo completo

## Problemas Frecuentes en Brain OS

| Problema | Causa Común | Fix |
|----------|-------------|-----|
| "ID no encontrado" en Notion | ID cambió o se borró la página | Actualizar `brain_config.md` |
| Timeout en Aula Virtual | Moodle lento o token expirado | Verificar MOODLE_TOKEN, reintentar |
| Dashboard desactualizado | `dashboard-sync` no se ejecutó | Correr manualmente |
| Playwright selector falla | UI de Moodle/NotebookLM cambió | Inspeccionar elemento, actualizar selector |
