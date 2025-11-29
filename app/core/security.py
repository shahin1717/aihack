from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import AdminUser
from app.core.auth import verify_token  # correct import

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> AdminUser:

    # Error template
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    # Extract email from JWT ("sub")
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    # Load admin from database
    admin = db.query(AdminUser).filter(AdminUser.email == email).first()

    if admin is None:
        raise credentials_exception

    return admin
