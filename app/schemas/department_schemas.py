from pydantic import BaseModel

class DepartmentCreate(BaseModel):
    name: str


