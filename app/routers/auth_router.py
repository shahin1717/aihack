from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import AdminUser
from app.schemas.auth_schemas import AdminRegister, AdminLogin, Token
from app.core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# ------------------------------------------------------
# ADMIN REGISTRATION
# ------------------------------------------------------
@router.post("/register", response_model=Token)
def register_admin(data: AdminRegister, db: Session = Depends(get_db)):

    # Check if admin already exists
    existing = db.query(AdminUser).filter(AdminUser.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists",
        )

    # Create new admin
    admin = AdminUser(
        email=data.email,
        hashed_password=get_password_hash(data.password)
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    # Create token
    token = create_access_token({"sub": admin.email})
    return Token(access_token=token)


# ------------------------------------------------------
# ADMIN LOGIN
# ------------------------------------------------------
@router.post("/login", response_model=Token)
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):

    admin = db.query(AdminUser).filter(AdminUser.email == data.email).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not verify_password(data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": admin.email})
    return Token(access_token=token)
