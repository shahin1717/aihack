import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session
from app.config import get_settings
from app.database.models import Campaign, CampaignRecipient, Employee

settings = get_settings()

def _build_email_html(
    campaign: Campaign,
    recipient_id: int,
    base_url: str,
    redirect_url: str,
    body_html: str | None = None,
) -> str:
    """
    Build HTML email body with:
    - original or personalized HTML body
    - tracking pixel
    - tracked CTA button
    """
    # Use personalized HTML if provided, otherwise the campaign default
    body = body_html or campaign.body_html

    pixel_url = f"{base_url}/track/open/{recipient_id}"
    pixel_tag = (
        f'<img src="{pixel_url}" width="1" height="1" '
        f'style="display:none;" alt="." />'
    )

    click_url = (
        f"{base_url}/track/click/{recipient_id}"
        f"?redirect={redirect_url}"
    )
    cta = (
        f'<p><a href="{click_url}" '
        f'style="color:#0b5ed7;font-weight:600;text-decoration:none;">'
        f'Open secure portal</a></p>'
    )

    return body + "\n" + cta + "\n" + pixel_tag

def send_campaign_emails(
    db: Session, campaign: Campaign, base_url: str,
    redirect_url="https://www.google.com"
):
    recipients = (
        db.query(CampaignRecipient)
        .filter(CampaignRecipient.campaign_id == campaign.id)
        .all()
    )

    if not recipients:
        return

    gmail_from = settings.SMTP_FROM_EMAIL or settings.SMTP_USER

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        for rec in recipients:
            employee = rec.employee or db.query(Employee).filter_by(id=rec.employee_id).first()
            if not employee:
                continue

            msg = MIMEMultipart("alternative")

            # Personalized subject or default
            subject = rec.personalized_subject or campaign.subject
            msg["Subject"] = subject
            msg["From"] = f"{campaign.sender_name} <{gmail_from}>"
            msg["To"] = employee.email

            # --- 🚀 MAKE BODY WITH TRACKING + CTA ---
            final_html = _build_email_html(
                campaign=campaign,
                recipient_id=rec.id,
                base_url=base_url,
                redirect_url=redirect_url,
                body_html=rec.personalized_body_html  # <-- AI-generated body
            )

            # Small plaintext fallback
            text_part = (
                f"Hello {employee.full_name},\n"
                f"Please view this message in HTML format."
            )

            msg.attach(MIMEText(text_part, "plain"))
            msg.attach(MIMEText(final_html, "html"))

            server.sendmail(
                gmail_from,
                [employee.email],
                msg.as_string(),
            )

            rec.email_sent = True
            rec.sent_at = datetime.utcnow()

        db.commit()