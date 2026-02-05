# 📥 Flujo de Captura - Aula Virtual

## Proceso de Descarga de Materiales

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   AULA VIRTUAL   │     │     BRAIN OS     │     │   NOTEBOOKLM     │
│  (Universidad)   │ ──► │  (Notion/Local)  │ ──► │   (Consultas)    │
└──────────────────┘     └──────────────────┘     └──────────────────┘
       │                        │                        │
       │ Descargas manual       │ Organiza y clasifica   │ Q&A inteligente
       │ PDFs, PPTs, docs       │ con metadatos          │ sobre materiales
       ▼                        ▼                        ▼
```

---

## Pasos para Cada Material

### 1. Descargar del Aula Virtual
Cuando el profesor suba material:
1. Descargar archivo (PDF, PPT, DOC, etc.)
2. Renombrar con formato: `[CURSO]_[TEMA]_[FECHA].ext`
   - Ejemplo: `ECO-AMB_Tema1_Intro_2026-02-10.pdf`

### 2. Registrar en Brain OS
Decir a Antigravity:
```
"Registra material de [Curso]: [Nombre del archivo]"
```

Brain OS automáticamente:
- Crea entrada en Notion (BD_RECURSOS)
- Clasifica por curso y tipo
- Vincula con tarea si aplica

### 3. Subir a NotebookLM (opcional)
Para materiales importantes de estudio:
```
"Agrega [archivo] al libro de [Curso] en NotebookLM"
```

---

## Tipos de Material

| Tipo | Extensión | Acción Recomendada |
|------|-----------|-------------------|
| Sílabo | PDF | ⭐ Subir a NotebookLM |
| Presentaciones | PPT/PDF | Subir si es tema clave |
| Lecturas | PDF | Subir a NotebookLM |
| Guías de tarea | PDF/DOC | Registrar en Notion |
| Anuncios | - | Crear recordatorio |

---

## Captura de Tareas del Aula Virtual

Cuando veas una tarea en el aula virtual:
```
"Nueva tarea: [Nombre] para [Curso], entrega [Fecha]"
```

Brain OS crea:
- Entrada en BD_TAREAS_MAESTRAS
- Recordatorios automáticos (7, 3, 1 días)
- Vinculación con el aporte correspondiente

---

## Estructura de Archivos Locales

```
carrera/semestres/2026-1/cursos/[CURSO]/recursos/
├── silabo.pdf
├── presentaciones/
│   ├── semana01_intro.pdf
│   └── semana02_tema.pdf
├── lecturas/
│   └── capitulo1.pdf
└── tareas/
    └── tarea1_enunciado.pdf
```

---

## Futuro: Automatización con API

> *Pendiente investigar si el aula virtual tiene API*

Si se encuentra API disponible:
- Sincronización automática de materiales
- Detección de nuevas tareas
- Alertas de anuncios del profesor
