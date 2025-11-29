from sqlalchemy.orm import Session
from datetime import datetime

from app.database.models import (
    Campaign,
    CampaignRecipient,
    Employee
)


# ------------------------------------------------------
# VALIDATE ALL EMPLOYEE IDS
# ------------------------------------------------------
def validate_employee_ids(db: Session, employee_ids: list[int]) -> list[Employee]:
    employees = (
        db.query(Employee)
        .filter(Employee.id.in_(employee_ids))
        .all()
    )

    if len(employees) != len(employee_ids):
        raise ValueError("Some employees do not exist")

    return employees


# ------------------------------------------------------
# CREATE CAMPAIGN
# ------------------------------------------------------
def create_campaign_record(
    db: Session,
    title: str,
    sender_name: str,
    sender_email: str,
    subject: str,
    body_html: str,
    admin_id: int
) -> Campaign:

    campaign = Campaign(
        title=title,
        sender_name=sender_name,
        sender_email=sender_email,
        subject=subject,
        body_html=body_html,
        admin_id=admin_id,
        created_at=datetime.utcnow()
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


# ------------------------------------------------------
# ATTACH EMPLOYEES TO CAMPAIGN
# ------------------------------------------------------
def attach_recipients_to_campaign(
    db: Session,
    campaign_id: int,
    employees: list[Employee]
) -> list[CampaignRecipient]:

    recipients = []

    for emp in employees:
        entry = CampaignRecipient(
            campaign_id=campaign_id,
            employee_id=emp.id
        )
        db.add(entry)
        recipients.append(entry)

    db.commit()
    return recipients


# ------------------------------------------------------
# FULL CAMPAIGN CREATION WORKFLOW
# ------------------------------------------------------
def create_full_campaign(
    db: Session,
    data,
    admin_id: int
) -> Campaign:

    # Validate employee list
    employees = validate_employee_ids(db, data.employee_ids)

    # Create campaign base record
    campaign = create_campaign_record(
        db=db,
        title=data.title,
        sender_name=data.sender_name,
        sender_email=data.sender_email,
        subject=data.subject,
        body_html=data.body_html,
        admin_id=admin_id
    )

    # Create recipient entries
    attach_recipients_to_campaign(db, campaign.id, employees)

    return campaign


# ------------------------------------------------------
# GET CAMPAIGN DETAILS FOR ADMIN
# ------------------------------------------------------
def get_campaign_owned(
    db: Session,
    campaign_id: int,
    admin_id: int
) -> Campaign:

    campaign = (
        db.query(Campaign)
        .filter(
            Campaign.id == campaign_id,
            Campaign.admin_id == admin_id
        )
        .first()
    )

    return campaign
