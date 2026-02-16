from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.predictions import router as predictions_router

app = FastAPI(title="Matchweek API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(predictions_router)

@app.get("/")
def health_check():
    return {"status": "ok"}