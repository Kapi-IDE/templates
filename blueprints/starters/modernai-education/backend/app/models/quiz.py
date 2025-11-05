from __future__ import annotations
from sqlalchemy import Column, JSON, Text, Enum, Boolean, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timedelta
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import Interval

from app.database import Base

class UserAnswer(Base):
    __tablename__ = 'user_answers'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quiz_session_id = Column(Integer, ForeignKey('quiz_sessions.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('quiz_questions.id'), nullable=False)
    user_response = Column(Text)
    correct = Column(Boolean)
    quiz_session = relationship("QuizSession", back_populates="answers")
    question = relationship("QuizQuestion")
    user = relationship("User", back_populates="answers")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    difficulty = Column(Integer)
    type = Column(String, index=True)  # e.g., 'mcq', 'open-ended', 'coding'
    question = Column(String, unique=True)
    
    choices = Column(JSONB, nullable=True)  # Store choices as JSON, optional
    correct_answer = Column(String, nullable=True)  # For open-ended or coding, this might be more complex
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



class QuizSession(Base):
    __tablename__ = 'quiz_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    current_question_index = Column(Integer, default=0)
    total_score = Column(Integer, default=0)  # Track user's score
    
    user = relationship("User", back_populates="quiz_sessions")
    answers = relationship("UserAnswer", back_populates="quiz_session", cascade="all, delete-orphan", lazy="dynamic")  # Add this line
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    time_taken = Column(Interval, default=timedelta(0))  # Track total time taken in the quiz
    is_active = Column(Boolean, default=True)  # Flag to indicate if the session is active

class Survey(Base):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True, index=True)
    surveyName = Column(String, index=True)
    surveyType = Column(String)
    question = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    responses = Column(JSONB)