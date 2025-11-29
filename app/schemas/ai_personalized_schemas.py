from pydantic import BaseModel
from typing import Optional


class AIEmailPersonalizedRequest(BaseModel):
    """
    Schema for personalized phishing email generation.
    This includes employee info, scenario info, and optional
    friend impersonation details.
    """

    # Employee information
    employee_name: str
    department: str
    role: str

    # Phishing scenario parameters
    scenario: str
    tone: str
    difficulty: str

    # Additional context for personalization
    personal_context: Optional[str] = None

    # Friend impersonation fields (optional)
    friend_name: Optional[str] = None
    friend_relation: Optional[str] = None
    friend_context: Optional[str] = None


class AIEmailResponse(BaseModel):
    """
    Standard AI wrapper output for phishing email generation.
    Contains subject and HTML body.
    """

    subject: str
    body_html: str
