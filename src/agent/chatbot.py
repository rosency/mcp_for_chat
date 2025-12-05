from anthropic import Anthropic
from src.agent.session import SessionManager, Session
from src.mcp.client import MCPClient
from src.config import MODEL

SYSTEM_PROMPT = """당신은 사실적이고 정확한 정보를 제공하는 유용한 보조 도구입니다.
웹 검색 및 웹 콘텐츠 수집 도구를 이용할 수 있습니다.

**다음 경우 반드시 도구를 사용하여 검색하십시오:**
- 날씨, 뉴스, 주가, 스포츠 경기 결과 등 실시간 정보
- 최신 사건, 유행, 트렌드에 대한 질문
- 특정 사실이나 통계 데이터 확인이 필요한 경우
- 현재 시점의 정보가 필요한 모든 질문

추측하지 말고 검색을 통해 확인하십시오.
무언가에 대해 확신이 서지 않을 때는 그 불확실성을 명확히 밝히십시오.
웹에서 얻은 정보를 사용할 때는 항상 출처를 인용하십시오.
채팅용 답변이므로 3문장 내외로 답변은 간결하고 유익하게 유지하십시오. """

class ChatbotAgent:
    def __init__(self, api_key: str, session_manager: SessionManager, mcp_client: MCPClient | None = None):
        self.client = Anthropic(api_key=api_key)
        self.session_manager = session_manager
        self.mcp_client = mcp_client
        self.model = MODEL

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
