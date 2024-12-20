from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime
#yuh
class ComplexityLevel(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class RetentionLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    topics = relationship("Topic", back_populates="user")
    study_sessions = relationship("StudySession", back_populates="user")
    schedules = relationship("Schedule", back_populates="user")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    complexity = Column(Enum(ComplexityLevel))
    retention_level = Column(Enum(RetentionLevel))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="topics")
    mindmaps = relationship("MindMap", back_populates="topic")

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    duration = Column(Integer)  # in minutes
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    
    user = relationship("User", back_populates="study_sessions")
    topic = relationship("Topic")

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer)  # 0-6 for Monday-Sunday
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    
    user = relationship("User", back_populates="schedules")
    topic = relationship("Topic")

class MindMap(Base):
    __tablename__ = "mindmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)  # JSON string storing mind map structure
    topic_id = Column(Integer, ForeignKey("topics.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    topic = relationship("Topic", back_populates="mindmaps")