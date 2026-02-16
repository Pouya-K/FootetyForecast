from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from app.database import Base
from datetime import datetime

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    match_date = Column(Date, nullable=False)
    matchweek = Column(Integer)

    home_win = Column(Float)
    draw = Column(Float)
    away_win = Column(Float)
    
    home_goals = Column(Float)
    away_goals = Column(Float)
    home_corners = Column(Float)
    away_corners = Column(Float)
    home_cards = Column(Float)
    away_cards = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)