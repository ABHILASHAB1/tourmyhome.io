from pydantic import BaseModel, Field

class WSMsgPayload(BaseModel):
    type: str = Field(..., description="'direct_message' or 'ping'")
    thread_id: str = None
    recipient_id: str = None
    content: str = None
