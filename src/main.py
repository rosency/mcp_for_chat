import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.routes import router, init_chatbot
from src.mcp.client import MCPClient
from src.mcp.tools import get_enabled_servers
from src.config import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

mcp_client: MCPClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mcp_client

    mcp_client = MCPClient()
    servers = get_enabled_servers()

    for name, config in servers.items():
        try:
            logger.info(f"Connecting to MCP server: {name}")
            await mcp_client.connect_server(
                name=name,
                command=config["command"],
                args=config["args"],
                env=config.get("env")
            )
            logger.info(f"Connected to {name}, tools: {list(mcp_client.tools.keys())}")
        except Exception as e:
            logger.warning(f"Failed to connect to {name}: {e}")

    init_chatbot(mcp_client if mcp_client.tools else None)
    logger.info(f"Chatbot initialized with {len(mcp_client.tools)} tools")

    yield

    if mcp_client:
        await mcp_client.close()
        logger.info("MCP connections closed")

app = FastAPI(
    title="MCP Fact Chatbot",
    description="A fact-based chatbot with MCP integration",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
