from datetime import datetime
from sqlalchemy.orm import Session

from app.database.models import CampaignRecipient, TrackingEvent, Employee


# ------------------------------------------------------
# RECORD EMAIL OPEN
# ------------------------------------------------------
def record_email_open(db: Session, recipient_id: int) -> CampaignRecipient:
    rec = (
        db.query(CampaignRecipient)
        .filter(CampaignRecipient.id == recipient_id)
        .first()
    )

    if not rec:
        return None

    # Only record once
    if not rec.email_opened:
        rec.email_opened = True
        rec.opened_at = datetime.utcnow()

        event = TrackingEvent(
            recipient_id=recipient_id,
            event_type="open"
        )
        db.add(event)

        # OPTIONAL: lower awareness score
        employee = (
            db.query(Employee)
            .filter(Employee.id == rec.employee_id)
            .first()
        )
        if employee:
            employee.awareness_score = max(0, employee.awareness_score - 2)

        db.commit()

    return rec


# ------------------------------------------------------
# RECORD LINK CLICK
# ------------------------------------------------------
def record_link_click(db: Session, recipient_id: int) -> CampaignRecipient:
    rec = (
        db.query(CampaignRecipient)
        .filter(CampaignRecipient.id == recipient_id)
        .first()
    )

    if not rec:
        return None

    # Only record once
    if not rec.link_clicked:
        rec.link_clicked = True
        rec.clicked_at = datetime.utcnow()

        event = TrackingEvent(
            recipient_id=recipient_id,
            event_type="click"
        )
        db.add(event)

        # OPTIONAL: lower awareness score more for clicking
        employee = (
            db.query(Employee)
            .filter(Employee.id == rec.employee_id)
            .first()
        )
        if employee:
            employee.awareness_score = max(0, employee.awareness_score - 10)

        db.commit()

    return rec


# ------------------------------------------------------
# GET TOTAL OPEN / CLICK STATS FOR A CAMPAIGN
# ------------------------------------------------------
def get_campaign_stats(db: Session, campaign_id: int):
    total = (
        db.query(CampaignRecipient)
        .filter(CampaignRecipient.campaign_id == campaign_id)
        .count()
    )

    opened = (
        db.query(CampaignRecipient)
        .filter(
            CampaignRecipient.campaign_id == campaign_id,
            CampaignRecipient.email_opened == True
        )
        .count()
    )

    clicked = (
        db.query(CampaignRecipient)
        .filter(
            CampaignRecipient.campaign_id == campaign_id,
            CampaignRecipient.link_clicked == True
        )
        .count()
    )

    return {
        "total": total,
        "opened": opened,
        "clicked": clicked,
        "open_rate": round((opened / total) * 100, 2) if total else 0,
        "click_rate": round((clicked / total) * 100, 2) if total else 0,
    }
