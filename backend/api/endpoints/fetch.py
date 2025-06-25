from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.config import SessionLocal
from crud.sensor_data import get_latest_bus_data, get_latest_queue_data

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/latest/bus")
def fetch_latest_bus(db: Session = Depends(get_db)):
    latest = get_latest_bus_data(db)
    if not latest:
        return {"message": "No bus data available"}
    return {
        "congestion_level": latest.congestion_level,
        "gender_ratio": latest.gender_ratio,
        "received_at": latest.received_at
    }

@router.get("/latest/queue")
def fetch_latest_queue(db: Session = Depends(get_db)):
    latest = get_latest_queue_data(db)
    if not latest:
        return {"message": "No queue data available"}
    return {
        "num_queue_people": latest.num_queue_people,
        "gender_ratio": latest.gender_ratio,
        "temperature": latest.temperature,
        "humidity": latest.humidity,
        "received_at": latest.received_at
    }
