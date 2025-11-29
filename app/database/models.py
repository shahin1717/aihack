from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


# -----------------------------------
# ADMIN USERS
# -----------------------------------
class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    campaigns = relationship("Campaign", back_populates="created_by_admin")


# -----------------------------------
# EMPLOYEES
# -----------------------------------
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    department = Column(String(255), nullable=True)
    awareness_score = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)

    received_campaigns = relationship("CampaignRecipient", back_populates="employee")


# -----------------------------------
# PHISHING CAMPAIGNS
# -----------------------------------
class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)

    # Email content sent to employees
    sender_name = Column(String(255), nullable=False)
    sender_email = Column(String(255), nullable=False)

    subject = Column(String(255), nullable=False)
    body_html = Column(Text, nullable=False)

    # Who created campaign?
    admin_id = Column(Integer, ForeignKey("admin_users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    created_by_admin = relationship("AdminUser", back_populates="campaigns")
    recipients = relationship("CampaignRecipient", back_populates="campaign")


# -----------------------------------
# CAMPAIGN → EMPLOYEE RELATION
# (which employee got which campaign)
# -----------------------------------
class CampaignRecipient(Base):
    __tablename__ = "campaign_recipients"

    id = Column(Integer, primary_key=True, index=True)

    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    email_sent = Column(Boolean, default=False)
    email_opened = Column(Boolean, default=False)
    link_clicked = Column(Boolean, default=False)

    sent_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)

    campaign = relationship("Campaign", back_populates="recipients")
    employee = relationship("Employee", back_populates="received_campaigns")

    tracking_events = relationship("TrackingEvent", back_populates="recipient")


# -----------------------------------
# TRACKING EVENTS (pixel opens / click logs)
# -----------------------------------
class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(Integer, primary_key=True, index=True)

    recipient_id = Column(Integer, ForeignKey("campaign_recipients.id"), nullable=False)
    event_type = Column(String(50), nullable=False)  # "open", "click"
    timestamp = Column(DateTime, default=datetime.utcnow)

    recipient = relationship("CampaignRecipient", back_populates="tracking_events")
