from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.database.models import Employee
from app.schemas.employee_schemas import EmployeeCreate, EmployeeOut
from app.core.auth import get_current_admin

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/add", response_model=EmployeeOut)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    db_employee = Employee(
        full_name=employee.full_name,
        email=employee.email,
        department=employee.department
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@router.get("/", response_model=List[EmployeeOut])
def list_employees(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    employees = db.query(Employee).all()
    return employees

