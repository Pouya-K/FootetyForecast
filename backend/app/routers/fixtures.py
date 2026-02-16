from fastapi import APIRouter
from app.services.fixtures_service import get_fixtures_by_week

router = APIRouter(prefix="/api", tags=["fixtures"])

@router.get("/fixtures")
def get_fixtures(week_offset: int = 0):
    """Get fixtures for a week. 0 = current, -1 = last week, 1 = next week."""
    data = get_fixtures_by_week(week_offset)
    return {
        "week_offset": week_offset,
        "week_start": data["week_start"],
        "week_end": data["week_end"],
        "count": len(data["fixtures"]),
        "fixtures": data["fixtures"],
    }