from sqlalchemy.orm import Session
from models.base import BusData, QueueData
from datetime import datetime

def save_bus_data(db: Session, congestion_level: int, gender_ratio: str, received_at: datetime):
    entry = BusData(
        congestion_level=congestion_level,
        gender_ratio=gender_ratio,
        received_at=received_at
    )
    db.add(entry)
    db.commit()

def save_queue_data(db: Session, num_queue_people: int, gender_ratio: str,
                    temperature: float, humidity: float, received_at: datetime):
    entry = QueueData(
        num_queue_people=num_queue_people,
        gender_ratio=gender_ratio,
        temperature=temperature,
        humidity=humidity,
        received_at=received_at
    )
    db.add(entry)
    db.commit()

def get_latest_bus_data(db: Session):
    return db.query(BusData).order_by(BusData.received_at.desc()).first()

def get_latest_queue_data(db: Session):
    return db.query(QueueData).order_by(QueueData.received_at.desc()).first()
