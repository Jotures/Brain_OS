# 🧠 Brain OS 2.0

Sistema de IA académico multi-semestre para maximizar tu rendimiento universitario.

**Meta**: Nota 20 en cada curso | **Versión**: 2.0

---

## 🚀 Inicio Rápido

```
/brain-os-study        → Planifica tu día de estudio
"¿Qué debo estudiar?"  → Diagnóstico con prioridades
"Modo Crisis [curso]"  → Estudio intensivo pre-examen
```

---

## 📂 Estructura & Organización
Este sistema usa una **Arquitectura Híbrida**: Notion es el índice ("La Biblioteca") y tu PC es el almacén físico.

### Estandar de Carpetas (Uni y Personal)
Todo curso debe seguir esta estructura simple:
```
[Nombre Curso]/
├── 01_Materiales/     # 📚 PDFs, PPTs, Libros (Lectura)
├── 02_Entregables/    # 📝 Tareas, Trabajos finales
├── 03_Notas/          # 🧠 Apuntes en Markdown/Txt
└── 04_Admin/          # 📄 Syllabus, Rúbricas
```

### Flujo de "Ingesta Inteligente"
1. **En PC**: Guardas archivo -> *"Brain OS, guarda esto en [Curso]"* -> Se mueve a carpeta + Sube a Notion.
2. **En Móvil**: Subes a Notion -> Al volver a PC: *"Sincroniza biblioteca"* -> Se descarga a tu carpeta.

---

## 📂 Directorios Principales (Root)

```
Brain_OS/
├── 📂 carrera/                    # 🎓 Universidad (Semestres)
│   └── semestres/2026-1/cursos/   # Cursos activos
├── 📂 cursos_personales/          # 🧘 Vida Personal (Inglés, Proyectos)
├── 📂 tools/                      # 🛠️ Herramientas (Pomodoro, etc)
├── 📂 sesiones/                   # 📝 Logs de estudio
├── 📂 skills/                     # 🧠 Habilidades AI
└── 📂 config/                     # ⚙️ Configuración
```

---

## 📊 Sistema de 3 Aportes

| Aporte | Periodo | Peso |
|--------|---------|------|
| Aporte 1 | Semanas 1-5 | 30% |
| Aporte 2 | Semanas 6-10 | 35% |
| Aporte 3 | Semanas 11-16 | 35% |

---

## 🔗 Integraciones

- **Notion MCP**: BD_TAREAS, BD_AREAS, BD_RECURSOS (bidireccional)
- **NotebookLM**: 7 libros (uno por curso)
- **Aula Virtual**: Materiales de Moodle
- **🍅 Pomodoro Timer**: Sesiones adaptativas con analytics

---

## ⏰ Recordatorios Automáticos

| Tipo | Tiempo | Acción |
|------|--------|--------|
| 🔴 Crítico | 1 día antes | Alerta urgente |
| 🟠 Prep | 3-5 días | Iniciar repaso |
| 🟡 Plan | 7 días | Crear plan |

---

## 🛠️ Skills Académicas (30+)

**Documentos**: `docx` · `xlsx` · `pptx` · `pdf`  
**Escritura**: `copywriting` · `copy-editing`  
**Planificación**: `brainstorming` · `writing-plans`  
**Investigación**: `notebooklm` 🔥 · `research-engineer`  
**Sistema**: `system-coordinator` · `dashboard-sync` 🆕

Uso: `"Usa la skill [nombre] para [tarea]"`

---

## 💡 Comandos

| Comando | Función |
|---------|---------|
| `¿Qué debo estudiar?` | Diagnóstico diario |
| `Registra sesión` | Guardar progreso |
| `Resume semana` | Análisis semanal |
| `Modo Crisis` | Estudio intensivo |
| `Inicia Pomodoro para [tema]` | Timer adaptativo 🆕 |
| `¿Cuántos pomodoros hoy?` | Analytics 🆕 |
