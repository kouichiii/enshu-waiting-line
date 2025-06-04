from fastapi import FastAPI, File, UploadFile, Request
import google.generativeai as genai
from dotenv import load_dotenv
import base64
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

app = FastAPI()

# DB設定
engine = create_engine("sqlite:///congestion.db")
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class CongestionData(Base):
    __tablename__ = "congestion"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String)
    location_id = Column(Integer)

Base.metadata.create_all(bind=engine)

# Gemini API設定
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # ハイフン (-) ではなくアンダースコア (_) を推奨
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# IPからlocation_idを判別する関数
def get_location_id_from_ip(ip: str) -> int:
    if ip.startswith("192.168.1."):
        return 1
    elif ip.startswith("192.168.2."):
        return 2
    else:
        return 0  # 未分類

@app.post("/upload/")
async def upload_photo(request: Request, file: UploadFile = File(...)):
    image_data = await file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    # IPからlocation_idを取得
    client_host = request.client.host
    location_id = get_location_id_from_ip(client_host)

    # Geminiへ画像＋プロンプト送信
    try:
        response = model.generate_content([
            "この画像の混雑状況を「大」「中」「小」で評価してください。",
            {
                "mime_type": "image/jpeg",
                "data": encoded_image
            }
        ])
        level = response.text.strip()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # データベースに保存
    session = SessionLocal()
    data = CongestionData(level=level, location_id=location_id)
    session.add(data)
    session.commit()
    session.close()

    return {"status": "success", "level": level, "location_id": location_id}

@app.get("/congestion/")
def get_latest_congestion():
    session = SessionLocal()
    latest = session.query(CongestionData).order_by(CongestionData.timestamp.desc()).first()
    session.close()
    if latest:
        return {
            "timestamp": latest.timestamp,
            "level": latest.level,
            "location_id": latest.location_id
        }
    else:
        return {"message": "データなし"}
