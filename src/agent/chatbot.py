import json
from anthropic import Anthropic
from src.agent.session import SessionManager, Session
from src.mcp.client import MCPClient

SYSTEM_PROMPT = """You are a helpful assistant that provides factual, accurate information.
You have access to tools for web search and fetching web content.
Use these tools when you need current information or to verify facts.
When you're unsure about something, clearly state that uncertainty.
Always cite your sources when using information from the web.
Keep responses concise and informative."""

class ChatbotAgent:
    def __init__(self, api_key: str, session_manager: SessionManager, mcp_client: MCPClient | None = None):
        self.client = Anthropic(api_key=api_key)
        self.session_manager = session_manager
        self.mcp_client = mcp_client
        self.model = "claude-sonnet-4-20250514"

    async def chat(self, session_id: str | None, message: str) -> tuple[str, Session, list[str]]:
        session = self.session_manager.get_or_create(session_id)
        self.session_manager.add_message(session.id, "user", message)

        messages = [{"role": m.role, "content": m.content} for m in session.messages]

        tools = self.mcp_client.get_tools_for_claude() if self.mcp_client else []
        sources = []

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=tools if tools else None
        )

        while response.stop_reason == "tool_use":
            tool_results = []
            assistant_content = response.content

            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input

                    try:
                        result = await self.mcp_client.call_tool(tool_name, tool_input)
                        result_text = self._extract_result_text(result)

                        if "url" in tool_input:
                            sources.append(tool_input["url"])

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result_text
                        })
                    except Exception as e:
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": f"Error: {str(e)}",
                            "is_error": True
                        })

            messages.append({"role": "assistant", "content": assistant_content})
            messages.append({"role": "user", "content": tool_results})

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=messages,
                tools=tools
            )

        assistant_message = ""
        for block in response.content:
            if hasattr(block, "text"):
                assistant_message += block.text

        self.session_manager.add_message(session.id, "assistant", assistant_message)

        return assistant_message, session, sources

    def _extract_result_text(self, result) -> str:
        if hasattr(result, "content"):
            texts = []
            for item in result.content:
                if hasattr(item, "text"):
                    texts.append(item.text)
            return "\n".join(texts)
        return str(result)
