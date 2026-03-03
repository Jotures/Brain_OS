# 📁 File Organizer — Contexto Brain OS

## Estructura Esperada de `carrera/`

Cada materia debe seguir esta estructura estándar:

```
carrera/semestres/2026-1/cursos/[MATERIA]/
├── 01_Materiales/       # PDFs, diapositivas, libros
├── 02_Tareas/           # Trabajos entregados (con nota si aplica)
├── 03_Apuntes/          # Notas personales, resúmenes
├── 04_Examenes/         # Material de exámenes y prácticos
└── 05_Proyectos/        # Trabajos largos, proyectos de curso (si aplica)
```

## Casos de Uso para Brain OS

### 1. Limpiar descargas de Aula Virtual
`aula-virtual` descarga archivos sin clasificar a una carpeta temporal. `file-organizer` los mueve al directorio correcto según la materia detectada.

### 2. Detectar duplicados entre cursos
Cuando el mismo PDF (ej: un artículo de Mankiw) se descarga para 2 cursos distintos, `file-organizer` detecta el duplicado y decide cuál conservar.

### 3. Auditoría semestral
Al inicio de cada semestre, ejecutar `file-organizer` sobre `carrera/` para:
- Archivar el semestre anterior a `carrera/semestres/2025-2/`
- Crear la estructura limpia para `carrera/semestres/2026-1/`
- Verificar integridad de la organización

## Protocolo de Uso

> ⚠️ **Siempre pedir confirmación antes de mover o eliminar archivos**

1. Identificar destino correcto según nombre de archivo y metadatos
2. Proponer plan de reorganización (mostrar cambios antes de ejecutar)
3. Esperar aprobación del usuario
4. Ejecutar + registrar en log

## Complemento con Otras Skills

- `aula-virtual` descarga → `file-organizer` clasifica → `library-manager` ingesta en Notion
- `cleanup-manager` (archiva materiales viejos) ← funciona en paralelo, no en conflicto
