from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from datetime import datetime
from src.core.entities.user import UserRole

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.BUYER, nullable=False)
    nafath_verified = Column(Boolean, default=False)
    trust_score = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
