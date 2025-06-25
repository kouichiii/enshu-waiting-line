#エンドポイント処理
#"uvicorn main:app --reload"でサーバを起動
#"http://localhost:8000/api/ping" にアクセスする

from fastapi import APIRouter, Form, File, UploadFile, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database.config import SessionLocal, engine
from models.base import Base
from crud.sensor_data import save_bus_data, save_queue_data
from services.image_analysis import analyze_image

router = APIRouter()

# 初回のみテーブル作成
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_data(
    device_id: str = Form(...),
    temperature: float = Form(...),
    humidity: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    received_at = datetime.now()
    image_bytes = await image.read()

    if device_id == "1":#工学部用のセンサがid=1
        # 仮の混雑度・男女比（ステップ4で Gemini API に置換）
        congestion_level, gender_ratio = analyze_image(image_bytes, device_id)
        if congestion_level is None:
            return {"error": "Image analysis failed"}
        save_bus_data(db, congestion_level, gender_ratio, received_at)#sensor_data.pyで定義した保存関数
    elif device_id == "2":#人間科学部用のセンサがid=2
        num_queue_people, gender_ratio = analyze_image(image_bytes, device_id)
        if num_queue_people is None:
            return {"error": "Image analysis failed"}
        save_queue_data(db, num_queue_people, gender_ratio, temperature, humidity, received_at)#sensor_data.pyで定義した保存関数
    else:
        return {"error": "Unknown device_id"}

    return {
        "message": "Data saved",
        "device_id": device_id,
        "received_at": received_at.isoformat()
    }
