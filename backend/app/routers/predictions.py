from fastapi import APIRouter, HTTPException
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(BASE_DIR, "ml", "model"))
sys.path.append(os.path.join(BASE_DIR, "ml", "features"))

from predict import predict_match, get_all_teams
from app.schemas.prediction import MatchRequest, MatchPrediction, MatchweekRequest, MatchweekResponse

router = APIRouter(prefix="/api", tags=["predictions"])

@router.get("/teams")
def list_teams():
    return get_all_teams()

@router.post("/predict", response_model = MatchPrediction)
def predict_single(match: MatchRequest):
    teams = get_all_teams()
    if match.home_team not in teams:
        raise HTTPException(status_code=400, detail=f"Home team {match.home_team} not found")
    if match.away_team not in teams:
        raise HTTPException(status_code=400, detail=f"Away team {match.away_team} not found")
    
    result = predict_match(match.home_team, match.away_team)
    return result

@router.post("/predict/matchweek", response_model=MatchweekResponse)
def predict_matchweek(request: MatchweekRequest):
    predictions = []

    for fixture in request.fixtures:
        result = predict_match(fixture.home_team, fixture.away_team)
        predictions.append(result)
    
    return {"predictions": predictions}

