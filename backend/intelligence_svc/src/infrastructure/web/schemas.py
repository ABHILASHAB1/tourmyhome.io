from pydantic import BaseModel, Field
from typing import List

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="UUID or 'new'")
    message: str = Field(..., max_length=1000)
    
class ListingOverview(BaseModel):
    id: str
    title: str
    price_sar: float

class ChatResponse(BaseModel):
    session_id: str
    ai_response_text: str
    suggested_listings: List[ListingOverview] = []
