from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import CampaignRecipient, Employee
from app.utils.awareness_score import apply_open_penalty, apply_click_penalty, apply_report_reward


def mark_opened(db: Session, campaign_id: int, employee_id: int):
    recipient = db.query(CampaignRecipient).filter(
        CampaignRecipient.campaign_id == campaign_id,
        CampaignRecipient.employee_id == employee_id
    ).first()
    
    if recipient and not recipient.opened:
        recipient.opened = True
        recipient.last_event_at = datetime.utcnow()
        
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if employee:
            employee.awareness_score = apply_open_penalty(employee.awareness_score)
        
        db.commit()


def mark_clicked(db: Session, campaign_id: int, employee_id: int):
    recipient = db.query(CampaignRecipient).filter(
        CampaignRecipient.campaign_id == campaign_id,
        CampaignRecipient.employee_id == employee_id
    ).first()
    
    if recipient and not recipient.clicked:
        recipient.clicked = True
        recipient.last_event_at = datetime.utcnow()
        
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if employee:
            employee.awareness_score = apply_click_penalty(employee.awareness_score)
        
        db.commit()


def mark_reported(db: Session, campaign_id: int, employee_id: int):
    recipient = db.query(CampaignRecipient).filter(
        CampaignRecipient.campaign_id == campaign_id,
        CampaignRecipient.employee_id == employee_id
    ).first()
    
    if recipient and not recipient.reported:
        recipient.reported = True
        recipient.last_event_at = datetime.utcnow()
        
        employee = db.query(Employee).filter(Employee.id == employee_id).first()
        if employee:
            employee.awareness_score = apply_report_reward(employee.awareness_score)
        
        db.commit()

