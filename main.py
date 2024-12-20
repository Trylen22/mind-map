from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
import schemas
import database
from typing import List
from database import engine
import uvicorn
import os
import subprocess

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Study Scheduler")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API routes
@app.post("/api/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/topics/", response_model=schemas.Topic)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    db_topic = models.Topic(**topic.dict())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@app.get("/api/topics/", response_model=List[schemas.Topic])
def get_topics(db: Session = Depends(get_db)):
    return db.query(models.Topic).all()

@app.get("/api/schedules/", response_model=List[schemas.Schedule])
def get_schedules(db: Session = Depends(get_db)):
    return db.query(models.Schedule).all()

@app.post("/api/schedules/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def serve():
    """Main function to start the server"""
    print("Starting Study Scheduler Server...")
    print("API Documentation available at: http://localhost:8000/docs")
    print("Frontend available at: http://localhost:3000")
    
    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    serve()