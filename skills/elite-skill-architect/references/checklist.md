# 📊 Checklist de Auditoría — 100 Puntos

> Usar este checklist para evaluar cualquier skill de Brain OS de forma estandarizada.

---

## 🎯 FUNCIONALIDAD (40 pts)

### Resolución del Problema (10 pts)

| Pts | Criterio |
|:---:|----------|
| 3 | ¿Tiene objetivo claro en SKILL.md? |
| 4 | ¿Resuelve el problema completamente? (no a medias) |
| 3 | ¿Funciona sin errores conocidos? |

### Niveles de Uso (10 pts)

| Pts | Criterio |
|:---:|----------|
| 3 | ¿Tiene modo básico? (funcionalidad mínima) |
| 4 | ¿Tiene modo intermedio? (funcionalidad completa) |
| 3 | ¿Tiene modo avanzado? (power user / opciones extra) |

> Si la skill no amerita 3 niveles por su naturaleza simple, otorgar 10/10 si cubre su alcance completamente.

### Manejo de Errores (10 pts)

| Pts | Criterio |
|:---:|----------|
| 5 | ¿Try-catch implementados en scripts? (o instrucciones de manejo en SKILL.md) |
| 5 | ¿Mensajes de error informativos? (no solo stack trace) |

> Si la skill no tiene scripts Python, evaluar si el SKILL.md instruye al agente sobre qué hacer cuando algo falla.

### Rollback/Undo (10 pts)

| Pts | Criterio | Notas |
|:---:|----------|-------|
| 2-10 | ¿Aplica rollback? | 2 pts si la skill no es riesgosa (solo lectura). 10 pts si es 🟡/🔴 y tiene rollback funcional |

> Escala: No riesgosa (solo lectura) = 2 pts gratis. Riesgosa sin rollback = 0 pts. Riesgosa con rollback = 10 pts.

---

## 📚 DOCUMENTACIÓN (25 pts)

### SKILL.md Completo (10 pts)

| Pts | Criterio |
|:---:|----------|
| 2 | ¿Existe SKILL.md con frontmatter válido? (name + description) |
| 3 | ¿Contenido sustancial? (>150 líneas o >2000 palabras) |
| 3 | ¿Incluye ejemplos de uso con inputs/outputs? |
| 2 | ¿Incluye outputs esperados en formato concreto? (JSON, tabla, etc.) |

### Pseudocódigo / Flujos (5 pts)

| Pts | Criterio |
|:---:|----------|
| 5 | ¿Incluye pseudocódigo o flujo paso a paso de funciones principales? |

### Tests Documentados (5 pts)

| Pts | Criterio |
|:---:|----------|
| 5 | ¿≥5 tests/escenarios documentados con inputs y outputs esperados? |

> Aceptable: sección de "Ejemplo de Interacción" con escenarios variados cuenta como tests.

### Casos de Uso (5 pts)

| Pts | Criterio |
|:---:|----------|
| 5 | ¿≥2 ejemplos con situaciones reales y outputs copiados/simulados? |

---

## 🔗 INTEGRACIÓN (20 pts)

### System-Coordinator (10 pts)

| Pts | Criterio |
|:---:|----------|
| 5 | ¿Mencionada en `system-coordinator/SKILL.md`? (lista de skills core) |
| 5 | ¿Aparece en auditorías / reportes del coordinator? |

### Convenciones del Proyecto (5 pts)

| Pts | Criterio |
|:---:|----------|
| 2 | ¿Sigue naming conventions? (`skills/{nombre}/`, kebab-case) |
| 2 | ¿Logs en formato JSON? (si aplica, si no, 2 pts gratis) |
| 1 | ¿Configs en `config/`? (si aplica, si no, 1 pt gratis) |

### README.md (5 pts)

| Pts | Criterio |
|:---:|----------|
| 5 | ¿Tiene entrada en el `README.md` del proyecto? |

---

## 🎨 UX DEL AGENTE (10 pts)

### Comandos Memorables (5 pts)

| Pts | Criterio |
|:---:|----------|
| 3 | ¿Comandos en lenguaje natural y claros? |
| 2 | ¿≥2 comandos distintos disponibles? |

### Outputs Informativos (3 pts)

| Pts | Criterio |
|:---:|----------|
| 3 | ¿Muestra progreso/resultados con formato? (no solo "OK" o texto plano) |

### Confirmaciones (2 pts)

| Pts | Criterio |
|:---:|----------|
| 2 | ¿Pide confirmación en operaciones riesgosas? (si no aplica, 2 pts gratis) |

---

## 🛡️ SEGURIDAD (5 pts)

### Zonas Críticas (2 pts)

| Pts | Criterio |
|:---:|----------|
| 1 | ¿Protege `carrera/semestres/` y datos académicos? |
| 1 | ¿Protege `skills/` y `config/` de modificaciones no intencionales? |

> Si la skill es de solo lectura, otorgar 2/2 automáticamente.

### Logs Auditables (2 pts)

| Pts | Criterio |
|:---:|----------|
| 2 | ¿Registra operaciones realizadas? (archivo de historial, log, o transcript) |

> Si la skill es puramente conversacional sin side effects, 2/2 gratis.

### Validación de Inputs (1 pt)

| Pts | Criterio |
|:---:|----------|
| 1 | ¿Valida inputs del usuario antes de operar? |

---

## 📊 Escala de Interpretación

| Score | Nivel | Emoji | Significado |
|:-----:|-------|:-----:|-------------|
| 90-100 | Elite | 🏆 | Referencia para otras skills |
| 75-89 | Excelente | ⭐ | Funciona muy bien, mejoras menores |
| 60-74 | Buena | ✅ | Funcional pero mejorable |
| 40-59 | Necesita mejoras | 🔧 | Brechas significativas |
| <40 | Rehacer | 🚨 | No cumple estándares mínimos |

---

## Notas para el Evaluador

1. **Ser justo con skills simples**: No todas necesitan 3 niveles de uso, rollback, o logs JSON. Usar las cláusulas "si no aplica, pts gratis".
2. **Contexto importa**: Una skill de solo lectura (ej: `brainstorming`) tiene requisitos de seguridad menores que una que modifica archivos (ej: `cleanup-manager`).
3. **Priorizar brechas**: Al reportar, ordenar brechas por impacto real, no por puntos perdidos.
4. **No inflactar scores**: Si algo no existe, es 0 — no inventar puntos parciales.
