import os

# SEARCH_PROVIDER: "duckduckgo" (default) or "brave"
SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "duckduckgo")

MCP_SERVERS = {
    "duckduckgo": {
        "command": "npx",
        "args": ["-y", "@nickclyde/duckduckgo-mcp-server"],
        "env": {},
        "enabled": SEARCH_PROVIDER == "duckduckgo"
    },
    "brave_search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env": {
            "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", "")
        },
        "enabled": SEARCH_PROVIDER == "brave" and bool(os.getenv("BRAVE_API_KEY"))
    },
    "fetch": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-fetch"],
        "env": {},
        "enabled": True
    }
}

def get_enabled_servers() -> dict:
    return {name: config for name, config in MCP_SERVERS.items() if config.get("enabled", True)}
