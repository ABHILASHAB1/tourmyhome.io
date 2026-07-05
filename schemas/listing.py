from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ListingBase(BaseModel):
    title: str
    description: Optional[str] = None
    price_sar: float
    image_url: str
    category: str

class ListingCreate(ListingBase):
    pass

class Listing(ListingBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
