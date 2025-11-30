# department_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import Department
from app.schemas.department_schemas import DepartmentCreate

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/")
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    dep = Department(name=data.name)
    db.add(dep)
    db.commit()
    db.refresh(dep)
    return dep

@router.get("/")
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()
