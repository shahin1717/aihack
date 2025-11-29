# ai_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.ai_schemas import AIGenerateRequest, AIGenerateResponse
from app.core.security import get_current_admin
from app.services.ai_generator import generate_email_for_employee

router = APIRouter(
    prefix="/ai",
    tags=["AI Generator"]
)


# ------------------------------------------------------
# GENERATE PHISHING EMAIL CONTENT USING AI
# ------------------------------------------------------
@router.post("/generate", response_model=AIGenerateResponse)
def generate_phishing_email(
    data: AIGenerateRequest,
    admin=Depends(get_current_admin)
):
    """
    Generates AI phishing email content.
    """
    try:
        result = generate_email_for_employee(
    employee_name="Employee",   # placeholder preview only
    topic=data.topic,
    tone=data.tone,
    difficulty=data.difficulty
)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return AIGenerateResponse(
        subject=result.get("subject"),
        body_html=result.get("body_html")
    )
