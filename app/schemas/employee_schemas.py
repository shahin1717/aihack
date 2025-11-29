from pydantic import BaseModel, EmailStr


# CREATE employee
class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    department: str | None = None


# READ employee (response)
class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    department: str | None
    awareness_score: int

    class Config:
        from_attributes = True
