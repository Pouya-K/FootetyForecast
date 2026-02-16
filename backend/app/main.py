from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.predictions import router as predictions_router
from app.routers.fixtures import router as fixtures_router
from app.database import engine, Base
from app.models.prediction import Prediction

app = FastAPI(title="Matchweek API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(predictions_router)
app.include_router(fixtures_router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "ok"}