from pydantic import BaseModel, EmailStr
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminUserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

