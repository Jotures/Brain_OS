# Checklist para Agregar Nuevo Curso

## Información del Curso

- **Nombre**: {{nombre}}
- **Código**: {{codigo}}
- **Tipo**: [ ] Universitario  [ ] Personal
- **Semestre**: {{semestre}}

---

## Paso 1: Notion

- [ ] Crear página en BD_AREAS
- [ ] Copiar ID de la página: `{{notion_id}}`

---

## Paso 2: NotebookLM

- [ ] Crear notebook en NotebookLM
- [ ] Copiar URL: `{{notebook_url}}`
- [ ] Determinar ID slug: `{{notebook_id}}`

---

## Paso 3: brain_config.md

Agregar en la sección correspondiente:

```yaml
CURSO_{{CODIGO}}:
  notion_id: "{{notion_id}}"
  notebook_id: "{{notebook_id}}"
  notebook_url: "{{notebook_url}}"
```

---

## Paso 4: notebooklm_registry.json

Agregar en "notebooks":

```json
{
    "id": "{{notebook_id}}",
    "name": "{{nombre}}",
    "curso_path": "carrera/semestres/{{semestre}}/cursos/{{codigo}}",
    "notion_id": "{{notion_id}}",
    "url": "{{notebook_url}}",
    "status": "active"
}
```

Agregar en "mapping":

```json
"{{codigo}}": "{{notebook_id}}"
```

---

## Paso 5: INICIO.md

Agregar en tabla de NotebookLM:

```markdown
| {{emoji}} {{nombre}} | "Consulta mi libro de {{nombre}}" |
```

---

## Paso 6: Crear Carpeta

```
carrera/semestres/{{semestre}}/cursos/{{codigo}}/
├── README.md
├── materiales/
├── evaluaciones/
└── sesiones/
```

---

## Verificación Final

- [ ] Ejecutar: "Verifica el sistema"
- [ ] Confirmar que todo está sincronizado
