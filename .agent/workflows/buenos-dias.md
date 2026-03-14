---
description: Macro-comando "Buenos días" — ejecuta la secuencia de boot matutino de Brain OS en automático. Activa cuando el usuario dice "Buenos días", "Buen día", "Empecemos", o similar.
---

# ☀️ Workflow Buenos Días — Boot Diario Brain OS

Secuencia atómica de 5 pasos que arranca el día del usuario. Se adapta automáticamente al tipo de día (L/MI vs MA/JU vs VI vs S/D) según el horario Bear.

---

## Detección del Tipo de Día

Antes de ejecutar, determinar el tipo de día con la fecha actual:

```yaml
LUNES/MIÉRCOLES:
  despertar: "08:30"
  boot_hora: "~09:00"
  tipo: "completo"
  clases_empiezan: "11:00"

MARTES/JUEVES:
  despertar: "06:00"
  boot_hora: "~14:30 (post-clases)"
  tipo: "simplificado"
  nota: "El usuario ya tuvo 6h de clases. Boot ligero."

VIERNES:
  despertar: "08:30"
  boot_hora: "~08:30"
  tipo: "completo"
  clases_empiezan: "09:00"

SÁBADO/DOMINGO:
  despertar: "09:00"
  boot_hora: "~09:30"
  tipo: "completo_relajado"
  nota: "Sin prisa. Café incluido."
```

---

## Secuencia de Boot

### Boot Completo (L/MI/VI/S/D)

// turbo
1. **Verificar sistema** — Ejecutar skill `system-coordinator` para confirmar integridad
   ```
   Verificar que Brain OS, skills y config están operativos.
   Si hay errores, reportar al usuario antes de continuar.
   Verificar NotebookLM v2 auth:
     python skills/notebooklm/scripts/notebooklm_client.py
     → Si "not_authenticated": avisar "NotebookLM v2 requiere login. Ejecuta: .venv\Scripts\notebooklm login"
     → Si "authenticated": reportar como ✅ en el resumen de boot
   ```

// turbo
2. **Sincronizar Aula Virtual** — Ejecutar skill `aula-virtual` completo
   ```powershell
   python tools/moodle/sync_moodle.py --mode full
   ```
   Reportar: nuevos archivos, tareas próximas, anuncios del profesor.

// turbo
3. **Actualizar dashboard** — Ejecutar skill `dashboard-sync`
   ```
   Actualizar INICIO.md con estado actual del sistema.
   ```

// turbo
4. **Diagnóstico del día** — Consultar Notion y generar plan
   ```
   Consultar BD_TAREAS_MAESTRAS → deadlines próximos 7 días.
   Calcular Pomodoros necesarios.
   Priorizar por urgencia (🔴 > 🟠 > 🟡).
   Presentar al usuario:
     "Hoy deberías enfocarte en: [materia], [X] Pomodoros sugeridos"
     "Deadlines próximos: [lista]"
   ```

5. **Hemingway Bridge** — Mostrar el hilo del día anterior
   ```
   Buscar la última nota de cierre (Hemingway Bridge) del usuario.
   Presentar: "Ayer dejaste este hilo: [contenido del bridge]"
   Si no hay bridge previo: "No hay hilo de ayer. ¿Por dónde quieres empezar?"
   ```

### Boot Simplificado (MA/JU — post-clases 14:30)

El usuario llega a casa después de 6 horas de clase (7am-1pm). No necesita verificación completa.

// turbo
1. **Actualizar dashboard** — Solo `dashboard-sync`

// turbo
2. **Diagnóstico rápido** — Plan para la tarde
   ```
   Consultar BD_TAREAS_MAESTRAS → solo tareas de hoy y mañana.
   Sugerir: "Tienes [X] horas hasta inglés (20:00). Sugiero [modo] para [materia]."
   Recordar: "Toma NSDR 15 min antes de empezar si estás cansado."
   ```

3. **Hemingway Bridge** — Mostrar hilo si existe

---

## Respuesta del Sistema

Al completar el boot, Brain OS presenta un resumen compacto:

```
☀️ Buenos días, Rubén — [Día], [Fecha]

📊 Sistema: ✅ Operativo
📥 Aula Virtual: [X nuevos archivos / sin novedades]
📋 Hoy: [materia prioritaria] — [modo sugerido] ([X] Pomodoros)

⏰ Deadlines:
  🔴 [tarea] — mañana
  🟠 [tarea] — en 3 días

🌉 Hilo de ayer: "[contenido del Hemingway Bridge]"

¿Empezamos con [materia]?
```

---

## Protocolo de Energía Matutino (recordar al usuario)

Si es **L/MI/VI/S/D** (boot completo):
- "☀️ ¿Ya tomaste luz natural? (10 min mejora tu cortisol matutino)"
- "☕ Café ideal a las [hora calculada = despertar + 90min]"

Si es **MA/JU** (boot simplificado):
- "😴 ¿Necesitas NSDR 15min? Llevas 6h de clases encima."

---

## Notas

- Si el sistema está offline (Notion/Moodle caídos), ejecutar solo pasos 4 y 5 con datos locales
- Si el usuario dice "Buenos días" a las 22:00, interpretar como boot nocturno y solo hacer pasos 4-5
- El workflow se integra con el Flujo Maestro v2 (Fase Boot)
