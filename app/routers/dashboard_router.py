# dashboard_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.connection import get_db
from app.database.models import Campaign, CampaignRecipient, Employee
from app.core.security import get_current_admin


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ------------------------------------------------------
# CAMPAIGN SUMMARY STATS
# ------------------------------------------------------
@router.get("/campaign/{campaign_id}")
def campaign_stats(
    campaign_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    # Check campaign belongs to admin
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.admin_id == admin.id)
        .first()
    )

    if not campaign:
        raise HTTPException(404, "Campaign not found")

    # Total recipients
    total = db.query(CampaignRecipient).filter(
        CampaignRecipient.campaign_id == campaign_id
    ).count()

    # Open count
    opened = db.query(CampaignRecipient).filter(
        CampaignRecipient.campaign_id == campaign_id,
        CampaignRecipient.email_opened == True
    ).count()

    # Click count
    clicked = db.query(CampaignRecipient).filter(
        CampaignRecipient.campaign_id == campaign_id,
        CampaignRecipient.link_clicked == True
    ).count()

    # Recipient details with join
    details = (
        db.query(
            Employee.full_name,
            Employee.email,
            CampaignRecipient.email_opened,
            CampaignRecipient.link_clicked,
            CampaignRecipient.opened_at,
            CampaignRecipient.clicked_at
        )
        .join(Employee, Employee.id == CampaignRecipient.employee_id)
        .filter(CampaignRecipient.campaign_id == campaign_id)
        .all()
    )

    return {
        "campaign_id": campaign.id,
        "title": campaign.title,
        "sender": f"{campaign.sender_name} <{campaign.sender_email}>",
        "total_recipients": total,
        "opened": opened,
        "clicked": clicked,
        "open_rate": round(opened / total * 100, 2) if total else 0,
        "click_rate": round(clicked / total * 100, 2) if total else 0,
        "details": [
            {
                "full_name": d[0],
                "email": d[1],
                "opened": d[2],
                "clicked": d[3],
                "opened_at": d[4],
                "clicked_at": d[5],
            }
            for d in details
        ],
    }
