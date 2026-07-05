from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities.message import Message, Thread

class MessageRepository(ABC):
    """Abstract base class (Port) for Message data access."""
    
    @abstractmethod
    async def save_message(self, message: Message) -> Message:
        pass
        
    @abstractmethod
    async def get_thread(self, thread_id: str) -> Optional[Thread]:
        pass
        
    @abstractmethod
    async def create_thread(self, thread: Thread) -> Thread:
        pass
