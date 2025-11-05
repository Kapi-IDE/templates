from __future__ import annotations
from sqlalchemy import Column, JSON, Text, Enum, Boolean, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
from app.database import Base

class LessonCategory(Base):
    __tablename__ = "lesson_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    level = Column(Integer, nullable=False)
 
    # Parent-Child relationship to create a hierarchy of categories
    parent_id = Column(Integer, ForeignKey('lesson_categories.id'), nullable=True)
    children = relationship("LessonCategory", backref="parent", remote_side=[id])
    lessons = relationship("Lesson", back_populates="category")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('lesson_categories.id'), nullable=False)
    order = Column(Integer, nullable=False)  # Order in which lessons are presented
    llm_prompt = Column(String) # This is a detailed prompt to give it to llm to help it provide help.
    category = relationship("LessonCategory", back_populates="lessons")
    contents = relationship("LessonContent", back_populates="lesson", lazy="dynamic")
    user_lessons = relationship("UserLesson", back_populates="lesson", lazy="dynamic")
    
class ContentType(enum.Enum):
    text = "text"
    image = "image"
    video = "video"
    code = "code"
    audio = "audio"
    
class LessonContent(Base):
    __tablename__ = "lesson_contents"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    content_type = Column(Enum(ContentType), nullable=False)
    
    # Text content stored directly, URLs for other content types
    text_content = Column(Text, nullable=True)  # For text content type
    content_url = Column(String, nullable=True)  # For image, video, audio URLs
    
    order = Column(Integer, nullable=False)  # Order in which content pieces appear

    lesson = relationship("Lesson", back_populates="contents")

class UserLesson(Base):
    __tablename__ = "user_lessons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    completed = Column(Boolean, default=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="user_lessons")
    lesson = relationship("Lesson", back_populates="user_lessons")
    issues = relationship("UserLessonIssue", back_populates="user_lesson")
    
class UserLessonIssue(Base):
    __tablename__ = "user_lesson_issues"

    id = Column(Integer, primary_key=True, index=True)
    user_lesson_id = Column(Integer, ForeignKey('user_lessons.id'), nullable=False)
    issue_description = Column(Text, nullable=False)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    user_lesson = relationship("UserLesson", back_populates="issues")