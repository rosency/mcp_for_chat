from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    sources: list[str] = []

class SessionInfo(BaseModel):
    session_id: str
    message_count: int
    created_at: float
    updated_at: float

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    tools_available: int = 0
