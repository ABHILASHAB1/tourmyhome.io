from pydantic import BaseModel, EmailStr, Field

class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="BUYER")
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class NafathWebhookRequest(BaseModel):
    user_id: str
    verification_status: str
    
class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    nafath_verified: bool
    trust_score: int
    
    class Config:
        from_attributes = True
