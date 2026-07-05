from abc import ABC, abstractmethod
from typing import Optional
from src.core.entities.chat_session import ChatSession

class ChatRepository(ABC):
    """Abstract base class (Port) for ChatSession data access (e.g., Redis)."""
    
    @abstractmethod
    async def save(self, session: ChatSession) -> None:
        pass
        
    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[ChatSession]:
        pass
