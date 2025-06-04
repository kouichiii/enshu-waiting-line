from fastapi import FastAPI, File, UploadFile, Request
import google.generativeai as genai
from dotenv import load_dotenv
import base64
import os
from sqlalchemy import create_engine, Column, Integer, DateTime
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
    people_count = Column(Integer)  # 修正: 数字として保存
    location_id = Column(Integer)

Base.metadata.create_all(bind=engine)

# Gemini API設定
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
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

    # クライアントIPからlocation_idを決定
    client_host = request.client.host
    location_id = get_location_id_from_ip(client_host)

    # Geminiへのプロンプト＋画像送信（画像とテキストは分離）
    try:
        response = model.generate_content([
"以下の画像を見て、行列に並んでいる人の人数を5の倍数で答えてください。",
    {
        "mime_type": "image/jpeg",
        "data": encoded_image
    },
"""
以下の注意事項に従ってください：
・行列に並んでいる人のみを数える  
・障害物があっても予測で見えない人数も含める  
・端が見えない場合は無視して見えている部分だけ評価する  
・出力は整数のみ（例：\"15\"）で、5の倍数に丸めて出力
"""
])
        people_count_str = response.text.strip()
        if not people_count_str.isdigit():
            raise ValueError("AIの出力が数値ではありません: " + people_count_str)
        people_count = int(people_count_str)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    # データベースに保存
    session = SessionLocal()
    data = CongestionData(people_count=people_count, location_id=location_id)
    session.add(data)
    session.commit()
    session.close()

    return {"status": "success", "people_count": people_count, "location_id": location_id}

@app.get("/congestion/")
def get_latest_congestion():
    session = SessionLocal()
    latest = session.query(CongestionData).order_by(CongestionData.timestamp.desc()).first()
    session.close()
    if latest:
        return {
            "timestamp": latest.timestamp,
            "people_count": latest.people_count,
            "location_id": latest.location_id
        }
    else:
        return {"message": "データなし"}
