from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database.connection import get_db
from app.database.models import Campaign, Employee, CampaignRecipient
from app.schemas.campaign_schemas import CampaignCreate, CampaignOut
from app.core.auth import get_current_admin
from app.services.campaign_service import create_campaign_recipients
from app.services.email_sender import send_campaign_emails

router = APIRouter(prefix="/campaign", tags=["campaign"])


@router.post("/create", response_model=CampaignOut)
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    db_campaign = Campaign(
        name=campaign.name,
        subject=campaign.subject,
        body_html=campaign.body_html
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    if campaign.employee_ids:
        create_campaign_recipients(db, db_campaign.id, campaign.employee_ids)
    
    return db_campaign


@router.post("/{campaign_id}/send")
def send_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    recipients = db.query(CampaignRecipient).filter(
        CampaignRecipient.campaign_id == campaign_id
    ).all()
    
    if not recipients:
        raise HTTPException(status_code=400, detail="No recipients found for this campaign")
    
    employee_ids = [r.employee_id for r in recipients]
    employees = db.query(Employee).filter(Employee.id.in_(employee_ids)).all()
    
    send_campaign_emails(campaign, employees)
    
    campaign.sent_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"Campaign sent to {len(employees)} employees"}


@router.get("/", response_model=List[CampaignOut])
def list_campaigns(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    campaigns = db.query(Campaign).all()
    return campaigns

