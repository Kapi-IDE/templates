from __future__ import annotations
from sqlalchemy import Column, Table, Text, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# Association table for many-to-many relationship between Workshop and User
workshop_participants = Table(
    "workshop_participants",
    Base.metadata,
    Column("workshop_id", Integer, ForeignKey("workshops.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)

class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    syllabus_link = Column(String, nullable=True)
    geography = Column(String, nullable=True)  # Location of the workshop
    payment_link = Column(String, nullable=True)
    cost = Column(Float, nullable=True)
    max_participants = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    participants = relationship("User", secondary=workshop_participants, backref="workshops")
    payment_history = relationship("WorkshopPaymentHistory", back_populates="workshop", lazy="dynamic")

class WorkshopPaymentHistory(Base):
    __tablename__ = "workshop_payment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False)  # succeeded, failed, refunded
    
    # Relationships
    workshop = relationship("Workshop", back_populates="payment_history")
    user = relationship("User", backref="workshop_payments")