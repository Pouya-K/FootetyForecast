from fastapi import APIRouter
from app.services.fixtures_service import get_weekly_fixtures

router = APIRouter(prefix="/api", tags=["fixtures"])

@router.get("/fixtures")
def get_fixtures():
    fixtures, date_from, date_to = get_weekly_fixtures()
    return {
        "week_start": date_from,
        "week_end": date_to,
        "count": len(fixtures),
        "fixtures": fixtures,
    }