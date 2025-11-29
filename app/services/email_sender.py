import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart"
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
    Build HTML email body with:
    - original campaign HTML body
    - tracking pixel (open tracking)
    - tracked CTA button (click tracking)
    """
    body = campaign.body_html

    # Open tracking pixel
    pixel_url = f"{base_url}/track/open/{recipient_id}"
    pixel_tag = (
        f'<img src="{pixel_url}" width="1" height="1" '
        f'style="display:none;" alt="." />'
    )

    # Click tracking link
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
    db: Session,
    campaign: Campaign,
    base_url: str,
    redirect_url: str = "https://www.google.com",
) -> None:
    """
    Send phishing simulation emails using Gmail SMTP.

    Gmail Requirements:
    - envelope MAIL FROM must be your real Gmail
    - message header From must also be your real Gmail
    - cannot spoof other sender addresses
    """

    recipients = (
        db.query(CampaignRecipient)
        .filter(CampaignRecipient.campaign_id == campaign.id)
        .all()
    )

    if not recipients:
        return

    # Connect to Gmail SMTP once
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        gmail_from = settings.SMTP_FROM_EMAIL or settings.SMTP_USER

        for rec in recipients:
            employee = rec.employee

            if employee is None:
                employee = (
                    db.query(Employee)
                    .filter(Employee.id == rec.employee_id)
                    .first()
                )
                if employee is None:
                    continue

            # Build email message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = campaign.subject

            # IMPORTANT: Gmail DOES NOT ALLOW SPOOFED EMAILS
            msg["From"] = f"{campaign.sender_name} <{gmail_from}>"
            msg["To"] = employee.email

            # Text fallback
            text_part = (
                f"Hello {employee.full_name},\n\n"
                f"Please view this email in HTML format."
            )

            # HTML body with tracking
            html_part = _build_email_html(
                campaign=campaign,
                recipient_id=rec.id,
                base_url=base_url.rstrip("/"),
                redirect_url=redirect_url,
            )

            msg.attach(MIMEText(text_part, "plain"))
            msg.attach(MIMEText(html_part, "html"))

            server.sendmail(
                gmail_from,
                [employee.email],
                msg.as_string(),
            )

            # Mark email as sent
            rec.email_sent = True
            rec.sent_at = datetime.utcnow()

        db.commit()
