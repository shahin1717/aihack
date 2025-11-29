from pydantic import BaseModel


class AIGenerateRequest(BaseModel):
    topic: str
    tone: str = "phishing"
    difficulty: str = "medium"


class AIGenerateResponse(BaseModel):
    subject: str
    body_html: str
