import asyncio
import os
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        self.sessions: dict[str, ClientSession] = {}
        self.tools: dict[str, dict] = {}
        self._contexts: dict[str, Any] = {}
        self._streams: dict[str, tuple] = {}

    async def connect_server(self, name: str, command: str, args: list[str], env: dict[str, str] | None = None):
        full_env = os.environ.copy()
        if env:
            full_env.update(env)

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=full_env
        )

        ctx = stdio_client(server_params)
        streams = await ctx.__aenter__()
        self._contexts[name] = ctx
        self._streams[name] = streams

        session = ClientSession(streams[0], streams[1])
        session_ctx = session.__aenter__()
        await session_ctx

        await session.initialize()
        self.sessions[name] = session

        tools_response = await session.list_tools()
        for tool in tools_response.tools:
            self.tools[tool.name] = {
                "server": name,
                "description": tool.description or "",
                "schema": tool.inputSchema
            }

        return session

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        tool_info = self.tools.get(tool_name)
        if not tool_info:
            raise ValueError(f"Tool {tool_name} not found")

        session = self.sessions.get(tool_info["server"])
        if not session:
            raise ValueError(f"Server for tool {tool_name} not connected")

        result = await session.call_tool(tool_name, arguments)
        return result

    def get_tools_for_claude(self) -> list[dict]:
        return [
            {
                "name": name,
                "description": info["description"],
                "input_schema": info["schema"]
            }
            for name, info in self.tools.items()
        ]

    async def close(self):
        for name, session in self.sessions.items():
            try:
                await session.__aexit__(None, None, None)
            except:
                pass

        for name, ctx in self._contexts.items():
            try:
                await ctx.__aexit__(None, None, None)
            except:
                pass

        self.sessions.clear()
        self._contexts.clear()
        self._streams.clear()
        self.tools.clear()
