# 🍅 Pomodoro Timer - Brain OS

Temporizador Pomodoro adaptativo integrado con Brain OS y Notion.

## Instalación

```powershell
cd tools/pomodoro
pip install -r requirements.txt
```

## Comandos

| Comando | Descripción |
|---------|-------------|
| `start --topic "X" --mode auto` | Inicia pomodoro |
| `pause` | Pausa el timer |
| `resume` | Reanuda timer pausado |
| `stop` | Detiene y registra sesión |
| `status` | Estado actual (JSON) |
| `history --period today/week/month` | Historial |
| `suggest --topic "X"` | Sugiere modo óptimo |

## Modos Disponibles

| Modo | Trabajo | Descanso corto | Descanso largo |
|------|---------|----------------|----------------|
| `default` | 25 min | 5 min | 15 min |
| `intensive` | 50 min | 10 min | 20 min |
| `light` | 15 min | 3 min | 10 min |
| `exam_prep` | 45 min | 8 min | 20 min |

## Ejemplos

```powershell
# Iniciar con tema (modo auto-detectado)
python pomodoro_timer.py start --topic "Cálculo - Integrales"

# Iniciar con modo específico
python pomodoro_timer.py start --topic "Inglés - Vocabulario" --mode light

# Ver estado
python pomodoro_timer.py status

# Ver historial de la semana
python pomodoro_timer.py history --period week
```

## Archivos

- `config.json` - Configuración de perfiles y reglas
- `state.json` - Estado actual del timer
- `history.json` - Historial de sesiones
- `sounds/` - Archivos de audio para notificaciones
