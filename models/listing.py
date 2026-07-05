from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price_sar = Column(Float)
    image_url = Column(String)
    category = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
