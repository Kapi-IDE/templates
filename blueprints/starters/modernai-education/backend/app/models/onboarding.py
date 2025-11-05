from __future__ import annotations
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class OnboardingType(enum.Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    REQUIRED = "required"

class OnboardingState(Base):
    __tablename__ = "onboarding_states"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=False)
    video_link = Column(String(255), nullable=True)
    prompt_to_llm = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    estimated_time = Column(Integer, nullable=True)  # Time in minutes
    resources = Column(JSON, nullable=True)  # Additional resources
    subscription_type = Column(Enum(OnboardingType), nullable=False, default=OnboardingType.REQUIRED)
    is_active = Column(Boolean, default=True)
    unlock_feature = Column(String(255), nullable=True)  # Feature unlocked upon completion
    
    # For gamification/progression
    skill_category = Column(String(100), nullable=True)
    elo_points = Column(Integer, default=0)  # ELO points earned upon completion
    
    user_onboarding_states = relationship("UserOnboardingState", back_populates="onboarding_state", lazy="dynamic")

class UserOnboardingState(Base):
    __tablename__ = "user_onboarding_states"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    onboarding_state_id = Column(Integer, ForeignKey('onboarding_states.id'), nullable=False)
    completion_status = Column(Boolean, default=False)
    start_date = Column(DateTime, server_default=func.now())
    completion_date = Column(DateTime, nullable=True)
    
    # Track engagement for retention analysis
    attempts = Column(Integer, default=0)
    last_activity = Column(DateTime, nullable=True)
    
    # For pair programming features
    completed_with_partner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    user = relationship("User", foreign_keys=[user_id], back_populates="user_onboarding_states")
    onboarding_state = relationship("OnboardingState", back_populates="user_onboarding_states")
    partner = relationship("User", foreign_keys=[completed_with_partner_id])
    
    # For gamification/progression tracking
    achievement_unlocked = Column(Boolean, default=False)
    feedback_rating = Column(Integer, nullable=True)  # User rating of this onboarding step