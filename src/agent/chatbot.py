from anthropic import Anthropic
from src.agent.session import SessionManager, Session

SYSTEM_PROMPT = """You are a helpful assistant that provides factual, accurate information.
When you're unsure about something, clearly state that uncertainty.
Keep responses concise and informative."""

class ChatbotAgent:
    def __init__(self, api_key: str, session_manager: SessionManager):
        self.client = Anthropic(api_key=api_key)
        self.session_manager = session_manager
        self.model = "claude-sonnet-4-20250514"

    async def chat(self, session_id: str | None, message: str) -> tuple[str, Session]:
        session = self.session_manager.get_or_create(session_id)

        self.session_manager.add_message(session.id, "user", message)

        messages = [{"role": m.role, "content": m.content} for m in session.messages]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        assistant_message = response.content[0].text
        self.session_manager.add_message(session.id, "assistant", assistant_message)

        return assistant_message, session
