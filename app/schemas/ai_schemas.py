from pydantic import BaseModel


class AIEmailRequest(BaseModel):
    scenario: str
    tone: str
    difficulty: str


class AIEmailResponse(BaseModel):
    subject: str
    body_html: str

