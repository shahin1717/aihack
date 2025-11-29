from pydantic import BaseModel, EmailStr


# ------------------------
# ADMIN REGISTRATION
# ------------------------
class AdminRegister(BaseModel):
    email: EmailStr
    password: str


# ------------------------
# ADMIN LOGIN
# ------------------------
class AdminLogin(BaseModel):
    email: EmailStr
    password: str


# ------------------------
# TOKEN RESPONSE
# ------------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
