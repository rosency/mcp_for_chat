import uuid
import time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Message:
    role: str
    content: str

@dataclass
class Session:
    id: str
    messages: list[Message] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

class SessionManager:
    def __init__(self, timeout: int = 3600):
        self._sessions: dict[str, Session] = {}
        self._timeout = timeout

    def create(self) -> Session:
        session = Session(id=str(uuid.uuid4()))
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> Optional[Session]:
        session = self._sessions.get(session_id)
        if session and (time.time() - session.updated_at) > self._timeout:
            self.delete(session_id)
            return None
        return session

    def get_or_create(self, session_id: Optional[str]) -> Session:
        if session_id:
            session = self.get(session_id)
            if session:
                return session
        return self.create()

    def add_message(self, session_id: str, role: str, content: str) -> None:
        session = self.get(session_id)
        if session:
            session.messages.append(Message(role=role, content=content))
            session.updated_at = time.time()

    def delete(self, session_id: str) -> bool:
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def cleanup_expired(self) -> int:
        now = time.time()
        expired = [sid for sid, s in self._sessions.items()
                   if (now - s.updated_at) > self._timeout]
        for sid in expired:
            del self._sessions[sid]
        return len(expired)
