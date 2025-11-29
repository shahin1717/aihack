from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CampaignCreate(BaseModel):
    name: str
    subject: str
    body_html: str
    employee_ids: Optional[List[int]] = None


class CampaignOut(BaseModel):
    id: int
    name: str
    subject: str
    body_html: str
    created_at: datetime
    sent_at: Optional[datetime]
    
    class Config:
        from_attributes = True

