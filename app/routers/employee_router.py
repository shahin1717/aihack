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
    department_id=data.department_id,  # ✔ correct
)

    db.add(employee)
    db.commit()
    db.refresh(employee)

    # RETURN A PROPER EmployeeResponse
    return EmployeeResponse(
        id=employee.id,
        full_name=employee.full_name,
        email=employee.email,
        department_name=employee.department.name if employee.department else None,
        awareness_score=employee.awareness_score
    )
# ------------------------------------------------------
# LIST EMPLOYEES
# ------------------------------------------------------
@router.get("/", response_model=list[EmployeeResponse])
def list_employees(
    department_id: int | None = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    q = db.query(Employee)

    if department_id is not None:
        q = q.filter(Employee.department_id == department_id)

    employees = q.order_by(Employee.id.desc()).all()
    return [
    EmployeeResponse(
        id=e.id,
        full_name=e.full_name,
        email=e.email,
        department_name=e.department.name if e.department else None,
        awareness_score=e.awareness_score
    )
    for e in employees
]

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
