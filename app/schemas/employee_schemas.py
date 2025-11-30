from pydantic import BaseModel, EmailStr


# CREATE employee
class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    department_id: int
    
# READ employee (response)
class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    email: str
    department_name: str | None
    awareness_score: int

    class Config:
        from_attributes = True