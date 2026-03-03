# 🔄 Workflow Automation — Contexto Brain OS

## Flujos Durables Críticos

### 1. Boot Diario ("Buenos días") — Secuencial
```
Paso 1: system-coordinator   → Verificar IDs e integridad
Paso 2: aula-virtual sync    → Descargar novedades de Moodle
Paso 3: dashboard-sync       → Regenerar INICIO.md
Paso 4: diagnóstico          → Consultar Notion → prioridades
Paso 5: Hemingway Bridge     → Leer último hilo de sesiones/
```
**Patrón**: Sequential Workflow
**Tolerancia a fallos**: Si paso 2 falla (Moodle caído), continuar con paso 3 usando datos del caché local.

### 2. Sincronización Aula Virtual → Notion — Orchestrator-Worker
```
Orchestrator: sync_full_local.py
├── Worker 1: download_files.py        → Moodle → archivos locales
├── Worker 2: sync_assignments.py      → Moodle → BD_TAREAS_MAESTRAS
└── Worker 3: sync_resources.py        → archivos locales → BD_RECURSOS
```
**Patrón**: Orchestrator-Worker
**Idempotencia**: Archivos ya descargados se saltan (checksum)

### 3. Progressive Summarization — Secuencial con Checkpoints
```
Capa 1: Captura (auto — al guardar archivo)
Capa 2: Negrita (usuario marca conceptos clave)
Capa 3: Resaltado (usuario selecciona lo más importante)
Capa 4: Resumen ejecutivo (agente genera síntesis)
```
**Patrón**: Sequential con checkpoint por capa
**Checkpoint**: Cada capa se guarda independientemente; no es necesario completar todas.

## Anti-Patrones a Evitar en Brain OS

| Anti-Patrón | Riesgo | Solución |
|-------------|--------|----------|
| Boot sin timeout | Se queda esperando Moodle infinitamente | Timeout 30s por paso |
| Sync sin idempotencia | Duplica archivos en Notion | Verificar antes de crear |
| Workflow monolítico | Un fallo en paso 2 mata todo | Try/except por paso; continuar |
