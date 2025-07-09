from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from database.config import Base

class BusData(Base):
    __tablename__ = "bus_data" #工学部用データベース
    id = Column(Integer, primary_key=True, index=True)
    congestion_level = Column(Integer)
    gender_ratio = Column(String)
    received_at = Column(DateTime, default=datetime.now)

class QueueData(Base):
    __tablename__ = "queue_data"#人間科学部前用データベース
    id = Column(Integer, primary_key=True, index=True)
    num_queue_people = Column(Integer)
    gender_ratio = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    received_at = Column(DateTime, default=datetime.now)
    predicted_comfort = Column(Integer, nullable=True)
    predicted_congestion = Column(Integer, nullable=True)
