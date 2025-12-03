import os

MCP_SERVERS = {
    "brave_search": {
        "command": "npx",
        "args": ["-y", "@anthropic-ai/mcp-server-brave-search"],
        "env": {
            "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", "")
        },
        "enabled": bool(os.getenv("BRAVE_API_KEY"))
    },
    "fetch": {
        "command": "npx",
        "args": ["-y", "@anthropic-ai/mcp-server-fetch"],
        "env": {},
        "enabled": True
    }
}

def get_enabled_servers() -> dict:
    return {name: config for name, config in MCP_SERVERS.items() if config.get("enabled", True)}
