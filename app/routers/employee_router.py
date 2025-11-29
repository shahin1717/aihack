# employee_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Employee
from app.schemas.employee_schemas import EmployeeCreate, EmployeeResponse
from app.core.security import get_current_admin

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


# ------------------------------------------------------
# CREATE EMPLOYEE
# ------------------------------------------------------
@router.post("/", response_model=EmployeeResponse)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    existing = db.query(Employee).filter(Employee.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this email already exists",
        )

    employee = Employee(
        full_name=data.full_name,
        email=data.email,
        department=data.department,
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# ------------------------------------------------------
# LIST EMPLOYEES
# ------------------------------------------------------
@router.get("/", response_model=list[EmployeeResponse])
def list_employees(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    employees = db.query(Employee).order_by(Employee.id.desc()).all()
    return employees


# ------------------------------------------------------
# GET SINGLE EMPLOYEE
# ------------------------------------------------------
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


# ------------------------------------------------------
# DELETE EMPLOYEE
# ------------------------------------------------------
@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    db.delete(employee)
    db.commit()

    return {"detail": "Employee deleted successfully"}
