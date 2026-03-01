---
name: library-manager
description: Gestiona la sincronización bidireccional entre archivos locales y la base de datos Notion 'BD_RECURSOS'. Maneja el ingreso inteligente de archivos (Smart Ingest) y aplica Progressive Summarization a materiales de estudio. Usar cuando el usuario diga "Guarda este archivo en [curso]", "Registra [X]", "Resume progresivamente [material]", "¿Qué materiales tengo de [curso]?", "Busca en mis recursos [tema]".
---

# 📚 Library Manager

> Puente entre el sistema de archivos local y el índice Notion (`BD_RECURSOS`) para materiales académicos.

## Cuándo Usar

- Mediante comandos: `"Guarda este archivo"`, `"Resume progresivamente"`, etc.
- Automáticamente cuando `aula-virtual` descarga nuevos materiales
- Cuando el usuario necesita buscar o consultar sus recursos académicos
- Pre-examen para activar Progressive Summarization

---

## Comandos

| Comando | Función |
|---------|---------|
| "Guarda este archivo en [Curso]" | Smart Ingest → mueve + registra en Notion |
| "Registra el PDF [X] en [Curso]" | Registra archivo existente en Notion |
| "Resume progresivamente [material]" | Aplica siguiente capa de Progressive Summarization |
| "Genera resumen ejecutivo de [material]" | Genera Capa 4 con mini-resumen + Active Recall |
| "¿Qué materiales tengo de [Curso]?" | Lista recursos de BD_RECURSOS filtrados por curso |
| "Busca en mis recursos [tema]" | Busca por título o tags en BD_RECURSOS |

---

## Funcionalidades

### 1. Smart Ingest (Capa 1)

Mueve un archivo desde una ubicación temporal a la estructura estándar y lo registra en Notion.

```
FLUJO:
1. Recibir archivo + curso destino
2. Determinar ruta destino:
   → carrera/semestres/2026-1/cursos/{curso}/materiales/{tipo}/
3. Clasificar tipo de archivo:
   → PDF → materiales/lecturas/
   → PPT/PPTX → materiales/diapositivas/
   → DOCX → materiales/documentos/
   → Otro → materiales/otros/
4. Mover archivo a ruta destino
5. Registrar en Notion BD_RECURSOS:
   → Título: nombre del archivo
   → Curso: curso destino
   → Tipo: clasificación automática
   → Ruta_local: ruta completa
   → Capa: 1 (captura)
   → Fecha_ingreso: timestamp actual
6. Confirmar al usuario
```

**Output esperado:**
```
✅ Archivo guardado:
   📄 "01-Programación Lineal.pdf"
   📁 carrera/semestres/2026-1/cursos/inv_operativa/materiales/lecturas/
   📊 Registrado en BD_RECURSOS (Capa 1: Captura)
```

### 2. Progressive Summarization

Sistema de 4 capas incrementales para procesar materiales de estudio:

| Capa | Qué Hace | Cuándo Aplicar | Trigger |
|:----:|----------|----------------|---------|
| **1: Captura** | Guardar sin procesar | Al recibir/descargar | `"Guarda este archivo"` |
| **2: Negrita** | Resaltar ideas principales | Primera lectura | Post-Pomodoro de lectura |
| **3: Resaltado** | Destacar lo crítico de las negritas | Pre-examen | `"Resume progresivamente"` |
| **4: Resumen** | Mini-resumen en tus palabras + Active Recall | Revisión final | `"Genera resumen ejecutivo"` |

```
FLUJO PROGRESSIVE SUMMARIZATION:

INPUT:  Archivo + capa actual (consultada en BD_RECURSOS)

SI capa_actual == 1:
   → Leer archivo completo
   → Identificar ideas principales (máx 30% del texto)
   → Generar versión con **negritas** en conceptos clave
   → Actualizar BD_RECURSOS → capa: 2

SI capa_actual == 2:
   → Leer versión con negritas
   → De las negritas, resaltar solo lo esencial (máx 10% del texto)
   → Generar versión con ==resaltado== sobre las negritas
   → Actualizar BD_RECURSOS → capa: 3

SI capa_actual == 3:
   → Leer versión resaltada
   → Generar resumen ejecutivo (3-5 oraciones)
   → Generar 3-5 preguntas de Active Recall (Bloom nivel 3-4)
   → Guardar resumen en materiales/resumenes/{nombre}_resumen.md
   → Actualizar BD_RECURSOS → capa: 4

SI capa_actual == 4:
   → "Este material ya tiene resumen completo."
   → Ofrecer: "¿Quieres regenerar el resumen?"
```

### 3. Consulta de Recursos

```
FLUJO:
1. Recibir query (curso y/o tema)
2. Consultar BD_RECURSOS con filtros:
   → Por curso: filter[Curso] == curso
   → Por tema: search en título/tags
3. Formatear resultado como tabla
4. Mostrar capa actual de cada recurso

OUTPUT:
| # | Material | Tipo | Capa | Última Actualización |
|---|----------|------|:----:|---------------------|
| 1 | Programación Lineal.pdf | Lectura | 🟢 4/4 | 2026-02-20 |
| 2 | Método Simplex.pptx | Diapositiva | 🟡 2/4 | 2026-02-15 |
| 3 | Ejercicios Resueltos.pdf | Lectura | 🔴 1/4 | 2026-02-10 |
```

---

## Manejo de Errores

| Error | Causa | Solución |
|-------|-------|----------|
| "Archivo no encontrado" | Ruta incorrecta o archivo eliminado | Verificar ruta, pedir al usuario que confirme |
| "Curso no existe" | Nombre de curso no mapeado | Listar cursos disponibles, pedir selección |
| "Notion no disponible" | Token expirado o sin conexión | Modo offline: mover archivo sin registrar, marcar para sync posterior |
| "Archivo ya existe" | Duplicado en carpeta destino | Preguntar: ¿reemplazar, renombrar, o cancelar? |
| "BD_RECURSOS no encontrada" | ID de DB incorrecto | Verificar brain_config.md para el ID correcto |

---

## Integración con Brain OS

| Evento | Skill Fuente | Acción del Library Manager |
|--------|-------------|----------------------------|
| Nuevo archivo desde Moodle | `aula-virtual` | Auto-ingest (Capa 1) |
| Post-Pomodoro de lectura | `pomodoro` | Sugerir Capa 2 si no se ha hecho |
| Pre-examen detectado | workflow `brain-os-study` | Sugerir Capas 3-4 |
| Consulta a NotebookLM | `notebooklm` | Ofrecer guardar respuesta como Capa 4 |
| Verificación del sistema | `system-coordinator` | Reportar stats de recursos por curso |

---

## Archivos de la Skill

```
skills/library-manager/
├── SKILL.md                    ← Este archivo
└── scripts/
    ├── ingest_file.py          ← Lógica de ingest y clasificación
    └── notion_adapter.py       ← Helper para queries a Notion BD_RECURSOS
```

---

## 🧪 Escenarios de Prueba

### Test 1: Ingest básico

```
Input:    "Guarda 01-Lectura.pdf en Investigación Operativa"
Espera:   Archivo movido + registrado en Notion
Verifica: - Archivo en carrera/.../inv_operativa/materiales/lecturas/
          - Entrada en BD_RECURSOS con capa: 1
Output:   Confirmación con ruta + emoji de tipo
```

### Test 2: Archivo duplicado

```
Input:    "Guarda 01-Lectura.pdf en IO" (ya existe)
Espera:   Detecta duplicado, pregunta al usuario
Verifica: NO sobrescribe sin confirmación
Output:   "⚠️ Ya existe. ¿Reemplazar, renombrar, o cancelar?"
```

### Test 3: Progressive Summarization Capa 2→3

```
Input:    "Resume progresivamente 01-Lectura.pdf"
Espera:   Lee BD_RECURSOS → capa actual es 2 → genera Capa 3
Verifica: - Resaltado generado correctamente
          - BD_RECURSOS actualizado a capa: 3
Output:   Versión resaltada + nota de progreso
```

### Test 4: Consulta de recursos

```
Input:    "¿Qué materiales tengo de Economía Ambiental?"
Espera:   Tabla con materiales filtrados por curso
Verifica: Tabla tiene columnas: Material, Tipo, Capa, Fecha
Output:   Tabla formateada con indicadores de capa (🟢/🟡/🔴)
```

### Test 5: Modo offline

```
Input:    "Guarda archivo.pdf en IO" (sin conexión a Notion)
Espera:   Archivo se mueve correctamente, registro pendiente
Verifica: - Archivo en carpeta correcta
          - Log de "pendiente de sync" generado
Output:   "✅ Archivo guardado. ⚠️ Registro en Notion pendiente (sin conexión)"
```
