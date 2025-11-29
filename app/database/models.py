from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    awareness_score = Column(Float, default=100.0)
    
    campaign_recipients = relationship("CampaignRecipient", back_populates="employee")


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body_html = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    recipients = relationship("CampaignRecipient", back_populates="campaign")


class CampaignRecipient(Base):
    __tablename__ = "campaign_recipients"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    opened = Column(Boolean, default=False)
    clicked = Column(Boolean, default=False)
    reported = Column(Boolean, default=False)
    last_event_at = Column(DateTime(timezone=True), nullable=True)
    
    campaign = relationship("Campaign", back_populates="recipients")
    employee = relationship("Employee", back_populates="campaign_recipients")

