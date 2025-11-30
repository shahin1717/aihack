# app/emails/emailsender.py

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session
from app.config import get_settings
from app.database.models import Campaign, CampaignRecipient, Employee

# NEW IMPORT
from app.emails.link_cleaner import remove_all_links  

settings = get_settings()


def _build_email_html(
    campaign: Campaign,
    recipient_id: int,
    base_url: str,
    redirect_url: str,
    body_html: str | None = None,
) -> str:
    """
    Build HTML body:
    - remove all untracked <a> links from AI text
    - inject tracking pixel
    - inject tracked CTA button
    """

    # select body (AI personalized or default)
    body = body_html or campaign.body_html

    # REMOVE ALL <a> LINKS FROM AI BODY
    body = remove_all_links(body)

    # OPEN TRACKING PIXEL
    pixel_url = f"{base_url}/track/open/{recipient_id}"
    pixel_tag = (
        f'<img src="{pixel_url}" width="1" height="1" '
        f'style="display:none;" alt="." />'
    )

    # CLICK TRACKING CTA
    click_url = (
        f"{base_url}/track/click/{recipient_id}"
        f"?redirect={redirect_url}"
    )
    cta_button = (
        f'<p><a href="{click_url}" '
        f'style="background:#0b5ed7;color:white;padding:12px 20px;border-radius:6px;'
        f'text-decoration:none;font-weight:600;">'
        f'Open secure portal</a></p>'
    )

    # FINAL CLEAN BODY + CTA + PIXEL
    return body + "\n" + cta_button + "\n" + pixel_tag


def send_campaign_emails(
    db: Session, 
    campaign: Campaign, 
    base_url: str,
    redirect_url="https://www.google.com"
):
    """
    Sends tracking-enabled phishing emails
    """

    recipients = (
        db.query(CampaignRecipient)
        .filter(CampaignRecipient.campaign_id == campaign.id)
        .all()
    )

    if not recipients:
        return

    smtp_from = settings.SMTP_FROM_EMAIL or settings.SMTP_USER

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        for rec in recipients:
            employee = (
                rec.employee or 
                db.query(Employee).filter_by(id=rec.employee_id).first()
            )
            if not employee:
                continue

            msg = MIMEMultipart("alternative")

            # personalized subject fallback
            subject = rec.personalized_subject or campaign.subject
            msg["Subject"] = subject
            msg["From"] = f"{campaign.sender_name} <{smtp_from}>"
            msg["To"] = employee.email

            # build HTML with tracking + CTA
            html_final = _build_email_html(
                campaign=campaign,
                recipient_id=rec.id,
                base_url=base_url,
                redirect_url=redirect_url,
                body_html=rec.personalized_body_html,
            )

            txt_fallback = (
                f"Hello {employee.full_name},\n"
                f"Please open this email in HTML format."
            )

            msg.attach(MIMEText(txt_fallback, "plain"))
            msg.attach(MIMEText(html_final, "html"))

            server.sendmail(
                smtp_from,
                [employee.email],
                msg.as_string(),
            )

            rec.email_sent = True
            rec.sent_at = datetime.utcnow()

        db.commit()
