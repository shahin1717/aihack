from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.database.models import Campaign, CampaignRecipient, Employee
from app.core.auth import get_current_admin

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/campaign/{campaign_id}/stats")
def get_campaign_stats(
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
    
    total = len(recipients)
    if total == 0:
        return {
            "campaign_id": campaign_id,
            "total_recipients": 0,
            "opened": 0,
            "clicked": 0,
            "reported": 0,
            "open_rate": 0.0,
            "click_rate": 0.0,
            "report_rate": 0.0
        }
    
    opened = sum(1 for r in recipients if r.opened)
    clicked = sum(1 for r in recipients if r.clicked)
    reported = sum(1 for r in recipients if r.reported)
    
    return {
        "campaign_id": campaign_id,
        "total_recipients": total,
        "opened": opened,
        "clicked": clicked,
        "reported": reported,
        "open_rate": round(opened / total * 100, 2),
        "click_rate": round(clicked / total * 100, 2),
        "report_rate": round(reported / total * 100, 2)
    }


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    total_employees = db.query(Employee).count()
    total_campaigns = db.query(Campaign).count()
    
    all_recipients = db.query(CampaignRecipient).all()
    total_recipients = len(all_recipients)
    
    if total_recipients == 0:
        return {
            "total_employees": total_employees,
            "total_campaigns": total_campaigns,
            "global_open_rate": 0.0,
            "global_click_rate": 0.0,
            "global_report_rate": 0.0
        }
    
    opened = sum(1 for r in all_recipients if r.opened)
    clicked = sum(1 for r in all_recipients if r.clicked)
    reported = sum(1 for r in all_recipients if r.reported)
    
    return {
        "total_employees": total_employees,
        "total_campaigns": total_campaigns,
        "global_open_rate": round(opened / total_recipients * 100, 2),
        "global_click_rate": round(clicked / total_recipients * 100, 2),
        "global_report_rate": round(reported / total_recipients * 100, 2)
    }

