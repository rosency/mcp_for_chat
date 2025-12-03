from fastapi import APIRouter, HTTPException
from src.api.models import ChatRequest, ChatResponse, SessionInfo, HealthResponse
from src.agent.chatbot import ChatbotAgent
from src.agent.session import SessionManager
from src.config import ANTHROPIC_API_KEY, SESSION_TIMEOUT

router = APIRouter()

session_manager = SessionManager(timeout=SESSION_TIMEOUT)
chatbot = ChatbotAgent(api_key=ANTHROPIC_API_KEY, session_manager=session_manager)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response_text, session = await chatbot.chat(request.session_id, request.message)
    return ChatResponse(
        session_id=session.id,
        response=response_text,
        sources=[]
    )

@router.get("/sessions/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
    session = session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionInfo(
        session_id=session.id,
        message_count=len(session.messages),
        created_at=session.created_at,
        updated_at=session.updated_at
    )

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    if not session_manager.delete(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}

@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")
