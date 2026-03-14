# 🔌 MCP (Model Context Protocol) Integration — Referencia Técnica

> Carga este archivo cuando el agente necesite conectar o crear servidores MCP.

## MCPAgent Pattern

```python
from mcp import Server, Tool

class MCPAgent:
    """
    Agent that can dynamically discover and use MCP tools.
    'Add a tool that...' pattern from Cline.
    """

    def __init__(self, llm):
        self.llm = llm
        self.mcp_servers = {}
        self.available_tools = {}

    def connect_server(self, name: str, config: dict) -> None:
        """Connect to an MCP server and discover its tools"""
        server = Server(config)
        self.mcp_servers[name] = server

        tools = server.list_tools()
        for tool in tools:
            self.available_tools[tool.name] = {
                "server": name,
                "schema": tool.schema
            }

    async def create_tool(self, description: str) -> str:
        """
        Create a new MCP server based on user description.
        Example: 'Add a tool that fetches Jira tickets'
        """
        # Generate MCP server code using LLM
        code = self.llm.generate(f"""
        Create a Python MCP server with a tool that does:
        {description}

        Use the FastMCP framework. Include proper error handling.
        Return only the Python code.
        """)

        server_name = self._extract_name(description)
        path = f"./mcp_servers/{server_name}/server.py"

        with open(path, 'w') as f:
            f.write(code)

        # Hot-reload: connect immediately without restart
        self.connect_server(server_name, {"path": path})

        return f"Created tool: {server_name}"
```

## Recursos Oficiales

- [Model Context Protocol Docs](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Anthropic Tool Use](https://docs.anthropic.com/claude/docs/tool-use)

## Servidores MCP en Brain OS

Los servidores MCP activos se configuran en `.agent/` y son cargados automáticamente por el agente. Ver `skills/system-coordinator/SKILL.md` para el listado oficial de integraciones.
