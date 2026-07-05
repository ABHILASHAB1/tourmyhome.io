from pydantic import BaseModel, Field
from typing import Optional

class CreateListingRequest(BaseModel):
    title: str = Field(..., max_length=100)
    description: str
    price_sar: float = Field(..., ge=1.0)
    category_id: Optional[str] = None
    
class UpdateListingRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    price_sar: Optional[float] = Field(None, ge=1.0)
    category_id: Optional[str] = None
    status: Optional[str] = None
    
class ListingResponse(BaseModel):
    id: str
    seller_id: str
    title: str
    description: str
    price_sar: float
    status: str
    
    class Config:
        from_attributes = True
