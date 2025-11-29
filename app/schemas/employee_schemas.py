from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    department: str


class EmployeeOut(BaseModel):
    id: int
    full_name: str
    email: str
    department: str
    awareness_score: float
    
    class Config:
        from_attributes = True

