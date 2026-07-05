from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class ThreadModel(Base):
    __tablename__ = "threads"
    
    id = Column(String, primary_key=True, index=True)
    listing_id = Column(String, index=True, nullable=False)
    buyer_id = Column(String, index=True, nullable=False)
    seller_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MessageModel(Base):
    __tablename__ = "direct_messages"
    
    id = Column(String, primary_key=True, index=True)
    thread_id = Column(String, ForeignKey("threads.id"), index=True, nullable=False)
    sender_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
