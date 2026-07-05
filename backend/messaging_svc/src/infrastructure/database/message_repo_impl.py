from typing import Optional
from sqlalchemy.orm import Session
from src.core.entities.message import Message, Thread
from src.application.interfaces.message_repository import MessageRepository
from src.infrastructure.database.models import MessageModel, ThreadModel

class SQLAMessageRepository(MessageRepository):
    """Concrete implementation of MessageRepository using SQLAlchemy."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    async def save_message(self, message: Message) -> Message:
        db_msg = MessageModel(
            id=message.id,
            thread_id=message.thread_id,
            sender_id=message.sender_id,
            content=message.content,
            is_read=message.is_read,
            created_at=message.created_at
        )
        self.db.add(db_msg)
        self.db.commit()
        self.db.refresh(db_msg)
        return message
        
    async def get_thread(self, thread_id: str) -> Optional[Thread]:
        pass
        
    async def create_thread(self, thread: Thread) -> Thread:
        pass
