# track_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.connection import get_db
from app.database.models import CampaignRecipient, TrackingEvent

router = APIRouter(
    prefix="/track",
    tags=["Tracking"],
)


# ------------------------------------------------------
# 1x1 TRANSPARENT PIXEL
# ------------------------------------------------------
PIXEL = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00"
    b"\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff\x21\xf9\x04\x01\x00"
    b"\x00\x00\x00\x2c\x00\x00\x00\x00"
    b"\x01\x00\x01\x00\x00\x02\x02\x4c"
    b"\x01\x00\x3b"
)


# ------------------------------------------------------
# EMAIL OPEN TRACKING (PIXEL)
# ------------------------------------------------------
@router.get("/open/{recipient_id}")
def track_open(
    recipient_id: int,
    db: Session = Depends(get_db)
):
    rec = db.query(CampaignRecipient).filter(CampaignRecipient.id == recipient_id).first()

    if not rec:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # If first time opening, record it
    if not rec.email_opened:
        rec.email_opened = True
        rec.opened_at = datetime.utcnow()

        event = TrackingEvent(
            recipient_id=recipient_id,
            event_type="open"
        )
        db.add(event)

        db.commit()

    # Return tracking pixel
    return Response(content=PIXEL, media_type="image/gif")


# ------------------------------------------------------
# LINK CLICK TRACKING
# ------------------------------------------------------
@router.get("/click/{recipient_id}")
def track_click(
    recipient_id: int,
    redirect: str | None = None,
    db: Session = Depends(get_db)
):
    rec = db.query(CampaignRecipient).filter(CampaignRecipient.id == recipient_id).first()

    if not rec:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # If first time click
    if not rec.link_clicked:
        rec.link_clicked = True
        rec.clicked_at = datetime.utcnow()

        event = TrackingEvent(
            recipient_id=recipient_id,
            event_type="click"
        )
        db.add(event)

        db.commit()

    # Redirect to phishing landing page OR default
    if redirect:
        return RedirectResponse(redirect)

    return {"detail": "Click tracked"}
