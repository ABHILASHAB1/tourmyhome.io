from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from datetime import datetime
from src.core.entities.listing import ListingStatus

Base = declarative_base()

class ListingModel(Base):
    __tablename__ = "listings"
    
    id = Column(String, primary_key=True, index=True)
    seller_id = Column(String, index=True, nullable=False)
    category_id = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_sar = Column(Float, nullable=False)
    status = Column(SQLEnum(ListingStatus), default=ListingStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
