from __future__ import annotations
from sqlalchemy import Column, JSON, Text, Enum, Boolean, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database import Base
from app.models.onboarding import UserOnboardingState
from app.models.programming import ProgrammingSession

class UserRoles(enum.Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"
    bd = "bd"

class SubscriptionTier(enum.Enum):
    free = "free"
    basic = "basic"  # $30/month
    premium = "premium"  # $500/3-month

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    
    # Role information
    role = Column(Enum(UserRoles), default=UserRoles.student)
    
    # Subscription information
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.free)
    subscription_start_date = Column(DateTime, nullable=True)
    subscription_end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Email verification
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    email_verification_sent_at = Column(DateTime, nullable=True)
    
    # Gamification and skill tracking
    elo_rating = Column(Integer, default=1000)  # Chess-like rating system
    skills_graph = Column(JSON, default={})  # Store skills as JSON object
    total_challenges_completed = Column(Integer, default=0)
    streak_count = Column(Integer, default=0)
    last_active_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Pod relationship (if user is in a learning pod)
    pod_id = Column(Integer, ForeignKey("learning_pods.id"), nullable=True)
    
    # Referral tracking
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    referrer = relationship("User", 
                           foreign_keys=[referred_by],
                           remote_side=[id],
                           backref="referred_direct_users")

    quiz_sessions = relationship("QuizSession", back_populates="user", lazy="dynamic")
    user_onboarding_states = relationship("UserOnboardingState", foreign_keys=[UserOnboardingState.user_id], back_populates="user", lazy="dynamic")
    user_lessons = relationship("UserLesson", back_populates="user", lazy="dynamic")
    answers = relationship("UserAnswer", back_populates="user", lazy="dynamic")
    programming_sessions = relationship("ProgrammingSession", foreign_keys=[ProgrammingSession.user_id], back_populates="user", lazy="dynamic")
    pod = relationship("LearningPod", back_populates="members")
    pod_members = relationship("LearningPodMember", back_populates="user", lazy="dynamic")
    payment_history = relationship("PaymentHistory", back_populates="user", lazy="dynamic")
    
    def is_subscription_active(self):
        """Check if user's subscription is currently active"""
        if self.subscription_tier == SubscriptionTier.free:
            return True
        if not self.subscription_end_date:
            return False
        return datetime.utcnow() <= self.subscription_end_date
        
class PaymentHistory(Base):
    __tablename__ = "payment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    subscription_tier = Column(Enum(SubscriptionTier), nullable=False)
    payment_method = Column(String, nullable=False)
    transaction_id = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False) # succeeded, failed, refunded
    
    user = relationship("User", back_populates="payment_history")

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referral_code = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, completed, rewarded
    
    # Track "Buddy boost" rewards
    referrer_reward_given = Column(Boolean, default=False)
    referred_reward_given = Column(Boolean, default=False)
    reward_type = Column(String, nullable=True)  # e.g., "free_month", "premium_content" 
    
    # Relationships
    referrer = relationship("User", foreign_keys=[referrer_id], backref="sent_referrals")
    referred = relationship("User", foreign_keys=[referred_id], backref="received_referral")

class EloHistory(Base):
    __tablename__ = "elo_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    previous_rating = Column(Integer, nullable=False)
    new_rating = Column(Integer, nullable=False)
    change = Column(Integer, nullable=False)  # Can be positive or negative
    reason = Column(String, nullable=False)  # e.g., "challenge_completion", "tournament_win"
    
    # If rating changed due to a programming session
    programming_session_id = Column(Integer, ForeignKey("programming_sessions.id"), nullable=True)
    
    # Optional opponent reference if rating changed due to pair programming
    opponent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="elo_history")
    opponent = relationship("User", foreign_keys=[opponent_id])
    programming_session = relationship("ProgrammingSession", backref="elo_changes")