from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.tracking_service import mark_opened, mark_clicked, mark_reported
from app.utils.tracking_pixel import get_tracking_pixel

router = APIRouter(prefix="/track", tags=["track"])


@router.get("/open/{campaign_id}/{employee_id}.png")
def track_open(campaign_id: int, employee_id: int, db: Session = Depends(get_db)):
    mark_opened(db, campaign_id, employee_id)
    return get_tracking_pixel()


@router.get("/click/{campaign_id}/{employee_id}")
def track_click(campaign_id: int, employee_id: int, db: Session = Depends(get_db)):
    mark_clicked(db, campaign_id, employee_id)
    return {
        "message": "This was a phishing simulation. You clicked on a suspicious link. Please be more careful in the future.",
        "training_url": "https://example.com/phishing-awareness-training"
    }


@router.get("/report/{campaign_id}/{employee_id}")
def track_report(campaign_id: int, employee_id: int, db: Session = Depends(get_db)):
    mark_reported(db, campaign_id, employee_id)
    return {
        "message": "Thank you for reporting this phishing attempt. Your awareness score has been increased."
    }

