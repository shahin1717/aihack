from pydantic import BaseModel, EmailStr
from typing import List


# Create Campaign
class CampaignCreate(BaseModel):
    title: str

    sender_name: str
    sender_email: EmailStr

    subject: str
    body_html: str

    employee_ids: List[int]  # which employees to target


# Response
class CampaignResponse(BaseModel):
    id: int
    title: str
    sender_name: str
    sender_email: EmailStr
    subject: str
    body_html: str

    class Config:
        from_attributes = True
