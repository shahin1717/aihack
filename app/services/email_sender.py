import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from sqlalchemy.orm import Session
from app.database.models import Campaign, Employee, CampaignRecipient
from app.config import get_settings

settings = get_settings()


def send_campaign_emails(campaign: Campaign, employees: List[Employee], base_url: str = "http://localhost:8000"):
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("Warning: SMTP credentials not configured. Skipping email send.")
        return
    
    for employee in employees:
        # Build tracking URLs
        open_url = f"{base_url}/track/open/{campaign.id}/{employee.id}.png"
        click_url = f"{base_url}/track/click/{campaign.id}/{employee.id}"
        report_url = f"{base_url}/track/report/{campaign.id}/{employee.id}"
        
        # Inject tracking pixel and links into email body
        email_body = campaign.body_html.replace("{click_url}", click_url)
        email_body = email_body.replace("{report_url}", report_url)
        
        # Add tracking pixel at the end
        email_body += f'<img src="{open_url}" width="1" height="1" style="display:none;" />'
        
        # Add report link if not already in body
        if "report" not in email_body.lower():
            email_body += f'<p><a href="{report_url}">Report Phishing</a></p>'
        
        # Create email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = campaign.subject
        msg["From"] = settings.SMTP_FROM_EMAIL or settings.SMTP_USER
        msg["To"] = employee.email
        
        html_part = MIMEText(email_body, "html")
        msg.attach(html_part)
        
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email to {employee.email}: {e}")

