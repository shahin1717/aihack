from sqlalchemy.orm import Session
from app.database.models import Campaign, CampaignRecipient, Employee


def create_campaign_recipients(db: Session, campaign_id: int, employee_ids: list):
    for employee_id in employee_ids:
        recipient = CampaignRecipient(
            campaign_id=campaign_id,
            employee_id=employee_id
        )
        db.add(recipient)
    db.commit()

