from pydantic import BaseModel
from typing import Optional
from models import ComplexityLevel, RetentionLevel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class TopicBase(BaseModel):
    title: str
    complexity: ComplexityLevel
    retention_level: RetentionLevel
    user_id: int

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int
    
    class Config:
        orm_mode = True 

class ScheduleBase(BaseModel):
    day_of_week: int
    start_time: datetime
    end_time: datetime
    user_id: int
    topic_id: int

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    
    class Config:
        orm_mode = True 