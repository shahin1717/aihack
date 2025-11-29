from fastapi import APIRouter, Depends
from app.schemas.ai_schemas import AIEmailRequest, AIEmailResponse
from app.services.ai_generator import generate_phishing_email
from app.core.auth import get_current_admin

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate-email", response_model=AIEmailResponse)
def generate_email(
    request: AIEmailRequest,
    current_admin = Depends(get_current_admin)
):
    return generate_phishing_email(request)

