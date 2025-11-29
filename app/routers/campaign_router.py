from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Campaign, Employee, CampaignRecipient
from app.schemas.campaign_schemas import CampaignCreate, CampaignResponse
from app.core.security import get_current_admin
from app.services.email_sender import send_campaign_emails

router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
)


# ------------------------------------------------------
# CREATE CAMPAIGN + SEND EMAILS
# ------------------------------------------------------
@router.post("/", response_model=CampaignResponse)
def create_campaign(
    data: CampaignCreate,
    request: Request,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    # Create campaign entry
    campaign = Campaign(
        title=data.title,
        sender_name=data.sender_name,
        sender_email=data.sender_email,
        subject=data.subject,
        body_html=data.body_html,
        admin_id=admin.id,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    # Validate employees exist
    employees = (
        db.query(Employee)
        .filter(Employee.id.in_(data.employee_ids))
        .all()
    )

    if len(employees) != len(data.employee_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some employees do not exist",
        )

    # Create CampaignRecipient entries
    recipients = []
    for emp in employees:
        link = CampaignRecipient(
            campaign_id=campaign.id,
            employee_id=emp.id,
        )
        db.add(link)
        recipients.append(link)

    db.commit()

    # Reload campaign with recipients
    db.refresh(campaign)

    # Base URL for tracking links, e.g. "http://localhost:8000"
    base_url = str(request.base_url).rstrip("/")

    # Send emails (simple redirect target for hackathon)
    send_campaign_emails(
        db=db,
        campaign=campaign,
        base_url=base_url,
        redirect_url="https://www.google.com",
    )

    return campaign


# ------------------------------------------------------
# LIST CAMPAIGNS
# ------------------------------------------------------
@router.get("/", response_model=list[CampaignResponse])
def list_campaigns(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    campaigns = (
        db.query(Campaign)
        .filter(Campaign.admin_id == admin.id)
        .order_by(Campaign.id.desc())
        .all()
    )
    return campaigns


# ------------------------------------------------------
# GET ONE CAMPAIGN
# ------------------------------------------------------
@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    campaign = (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id, Campaign.admin_id == admin.id)
        .first()
    )

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    return campaign
