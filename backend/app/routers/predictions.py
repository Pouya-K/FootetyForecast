from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.prediction import Prediction
from typing import List
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(BASE_DIR, "ml", "model"))
sys.path.append(os.path.join(BASE_DIR, "ml", "features"))

from predict import predict_match, get_all_teams
from app.schemas.prediction import MatchRequest, MatchPrediction, MatchweekRequest, MatchweekResponse

router = APIRouter(prefix="/api", tags=["predictions"])

@router.get("/predictions", response_model=List[MatchPrediction])
def get_predictions(matchweek: int, db: Session = Depends(get_db)):
    predictions = db.query(Prediction).filter(
        Prediction.matchweek == matchweek
    ).all()
    return predictions

@router.get("/teams")
def list_teams():
    return get_all_teams()

@router.post("/predict", response_model=MatchPrediction)
def predict_single(match: MatchRequest, db: Session = Depends(get_db)):
    teams = get_all_teams()
    if match.home_team not in teams:
        raise HTTPException(status_code=400, detail=f"Home team {match.home_team} not found")
    if match.away_team not in teams:
        raise HTTPException(status_code=400, detail=f"Away team {match.away_team} not found")
    
    # Check for duplicate
    existing = db.query(Prediction).filter(
        Prediction.home_team == match.home_team,
        Prediction.away_team == match.away_team,
        Prediction.match_date == match.match_date
    ).first()

    if existing:
        return existing
    
    result = predict_match(match.home_team, match.away_team)
    result["match_date"] = match.match_date

    db_prediction = Prediction(**result)
    db.add(db_prediction)
    db.commit()
    return result

@router.post("/predict/matchweek", response_model=MatchweekResponse)
def predict_matchweek(request: MatchweekRequest, db: Session = Depends(get_db)):
    predictions = []

    for fixture in request.fixtures:
        # Check for duplicate
        existing = db.query(Prediction).filter(
            Prediction.home_team == fixture.home_team,
            Prediction.away_team == fixture.away_team,
            Prediction.match_date == fixture.match_date
        ).first()

        if existing:
            predictions.append(existing)
        else:
            result = predict_match(fixture.home_team, fixture.away_team)
            result["match_date"] = fixture.match_date

            db_prediction = Prediction(**result)
            db.add(db_prediction)
            predictions.append(result)
    
    db.commit()
    return {"predictions": predictions}
