from pydantic import BaseModel
from typing import List

class MatchRequest(BaseModel):
    home_team: str
    away_team: str

class MatchPrediction(BaseModel):
    home_team: str
    away_team: str 
    home_win: float
    draw: float
    away_win: float
    home_goals: float
    away_goals: float
    home_corners: float
    away_corners: float
    home_cards: float
    away_cards: float

class MatchweekRequest(BaseModel):
    fixtures: List[MatchRequest]

class MatchweekResponse(BaseModel):
    predictions: List[MatchPrediction]