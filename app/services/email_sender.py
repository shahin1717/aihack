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
) -> str:
    """
    Build HTML body:
    - original campaign.body_html
    - tracking pixel
    - tracked CTA link
    """
    body = campaign.body_html

    # Tracking pixel for opens
    pixel_url = f"{base_url}/track/open/{recipient_id}"
    pixel_tag = (
        f'<img src="{pixel_url}" width="1" height="1" '
        f'style="display:none;" alt="." />'
    )

    # Tracked click link (simple for hackathon)
    click_url = (
        f"{base_url}/track/click/{recipient_id}"
        f"?redirect={redirect_url}"
    )
    cta = (
        f'<p><a href="{click_url}" '
        f'style="color:#0b5ed7;text-decoration:none;font-weight:600;">'
        f'Open secure portal</a></p>'
    )

    return body + "\n" + cta + "\n" + pixel_tag


def send_campaign_emails(
    db: Session,
    campaign: Campaign,
    base_url: str,
    redirect_url: str = "https://www.google.com",
) -> None:
    """
    Send phishing emails for a campaign to all its recipients.

    - base_url: e.g. "http://localhost:8000" or your deployed URL (without trailing slash)
    - redirect_url: where to send user AFTER click tracking
    """

    # Get all recipients for this campaign (with employee loaded)
    recipients = (
        db.query(CampaignRecipient)
        .filter(CampaignRecipient.campaign_id == campaign.id)
        .all()
    )

    if not recipients:
        return

    # Setup SMTP connection once per campaign
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        for rec in recipients:
            # Load employee
            employee = rec.employee
            if employee is None:
                employee = (
                    db.query(Employee)
                    .filter(Employee.id == rec.employee_id)
                    .first()
                )
                if employee is None:
                    continue

            # Build email
            msg = MIMEMultipart("alternative")
            msg["Subject"] = campaign.subject
            # Visible From: spoofed sender chosen by admin
            msg["From"] = f"{campaign.sender_name} <{campaign.sender_email}>"
            msg["To"] = employee.email

            # Plain text fallback
            text_part = (
                f"Hello {employee.full_name},\n\n"
                f"Please view this email in HTML format."
            )

            html_part = _build_email_html(
                campaign=campaign,
                recipient_id=rec.id,
                base_url=base_url.rstrip("/"),
                redirect_url=redirect_url,
            )

            msg.attach(MIMEText(text_part, "plain"))
            msg.attach(MIMEText(html_part, "html"))

            # Envelope sender is your real Gmail / SMTP user
            envelope_from = settings.SMTP_FROM_EMAIL or settings.SMTP_USER

            # Send email
            server.sendmail(
                envelope_from,
                [employee.email],
                msg.as_string(),
            )

            # Mark as sent
            rec.email_sent = True
            rec.sent_at = datetime.utcnow()

        # Commit DB changes after loop
        db.commit()
