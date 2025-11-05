from __future__ import annotations
from sqlalchemy import Column, JSON, Text, Enum, Boolean, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timedelta
from app.database import Base

class DifficultyLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ProgrammingChallenge(Base):
    __tablename__ = "programming_challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER)
    requirements = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=True)
    solution_template = Column(Text, nullable=True)
    test_cases = Column(JSON, nullable=False)  # JSON array of test cases
    elo_points = Column(Integer, default=10)  # Points awarded upon completion
    category = Column(String, nullable=False)  # AI domain/technology category
    estimated_time = Column(Integer, nullable=False)  # Estimated minutes to complete
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    programming_sessions = relationship("ProgrammingSession", back_populates="challenge", lazy="dynamic")

class ProgrammingSession(Base):
    __tablename__ = "programming_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("programming_challenges.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null if AI partner
    is_ai_partner = Column(Boolean, default=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    code_solution = Column(Text, nullable=True)
    performance_score = Column(Float, nullable=True)  # Rating of performance in this session
    
    # Session metrics for ELO calculation
    time_spent = Column(Integer, nullable=True)  # Time in seconds
    lines_of_code = Column(Integer, nullable=True)
    test_cases_passed = Column(Integer, nullable=True)
    
    # For pair programming matchmaking
    scheduled_time = Column(DateTime, nullable=True)
    status = Column(String(50), default="scheduled")  # scheduled, active, completed, cancelled
    
    user = relationship("User", foreign_keys=[user_id], back_populates="programming_sessions")
    partner = relationship("User", foreign_keys=[partner_id])
    challenge = relationship("ProgrammingChallenge", back_populates="programming_sessions")

class LearningPod(Base):
    __tablename__ = "learning_pods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    # Pod metrics and achievements
    achievement_points = Column(Integer, default=0)
    challenges_completed = Column(Integer, default=0)
    
    # Relationships
    pod_members = relationship("LearningPodMember", back_populates="pod", lazy="dynamic")
    members = relationship("User", back_populates="pod", lazy="dynamic")

class LearningPodMember(Base):
    __tablename__ = "learning_pod_members"
    
    id = Column(Integer, primary_key=True, index=True)
    pod_id = Column(Integer, ForeignKey("learning_pods.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    
    pod = relationship("LearningPod", back_populates="pod_members")
    user = relationship("User", back_populates="pod_members")