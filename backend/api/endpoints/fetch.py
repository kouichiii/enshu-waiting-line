from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.config import SessionLocal
from crud.sensor_data import get_latest_bus_data, get_latest_queue_data
from services.image_analysis import predict_congestion_and_comfort

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

@router.get("/status")
async def fetch_latest_data(db: Session = Depends(get_db)):
    bus = get_latest_bus_data(db)
    queue = get_latest_queue_data(db)

    if not bus or not queue:
        return {"error": "データが不足しています"}

    # 男女比・温湿度の平均で推測（単純な例）
    congestion_level = bus.congestion_level
    num_queue_people = queue.num_queue_people
    gender_ratio_bus = bus.gender_ratio
    gender_ratio_queue = queue.gender_ratio
    temperature = queue.temperature
    humidity = queue.humidity

    comfort, predicted_congestion = predict_congestion_and_comfort(
        congestion_level, num_queue_people, gender_ratio_bus, gender_ratio_queue, temperature, humidity
    )

    return {
        "bus": {
            "congestion_level": bus.congestion_level,
            "gender_ratio": bus.gender_ratio,
            "received_at": bus.received_at
        },
        "queue": {
            "num_queue_people": queue.num_queue_people,
            "temperature": temperature,
            "humidity": humidity,
            "gender_ratio": queue.gender_ratio,
            "received_at": queue.received_at
        },
        "predicted": {
            "comfortability": comfort,
            "congestion_level": predicted_congestion
        }
    }