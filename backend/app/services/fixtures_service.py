import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_KEY")
BASE_URL = "https://api.football-data.org/v4"

# football-data.org uses "FC" suffixed names, our data uses short names
TEAM_NAME_MAP = {
    "Manchester City FC": "Man City",
    "Manchester United FC": "Man United",
    "Newcastle United FC": "Newcastle",
    "Wolverhampton Wanderers FC": "Wolves",
    "Nottingham Forest FC": "Nott'm Forest",
    "West Ham United FC": "West Ham",
    "Tottenham Hotspur FC": "Tottenham",
    "Leicester City FC": "Leicester",
    "Brighton & Hove Albion FC": "Brighton",
    "Arsenal FC": "Arsenal",
    "Chelsea FC": "Chelsea",
    "Liverpool FC": "Liverpool",
    "Aston Villa FC": "Aston Villa",
    "Everton FC": "Everton",
    "Fulham FC": "Fulham",
    "AFC Bournemouth": "Bournemouth",
    "Crystal Palace FC": "Crystal Palace",
    "Brentford FC": "Brentford",
    "Ipswich Town FC": "Ipswich",
    "Southampton FC": "Southampton",
    "Leeds United FC": "Leeds",
    "Sunderland AFC": "Sunderland",
    "Burnley FC": "Burnley",
}

def map_team_name(api_name):
    return TEAM_NAME_MAP.get(api_name, api_name)

def get_week_range():
    """Get Monday-Sunday of the current week."""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())  # weekday() returns 0=Monday
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

def get_weekly_fixtures():
    """Get all Premier League games this week (Monday-Sunday)."""
    date_from, date_to = get_week_range()

    response = requests.get(
        f"{BASE_URL}/competitions/PL/matches",
        headers={"X-Auth-Token": API_KEY},
        params={
            "dateFrom": date_from,
            "dateTo": date_to,
        }
    )

    if response.status_code != 200:
        raise Exception(f"football-data.org error: {response.status_code} - {response.text}")

    data = response.json()
    fixtures = []

    for match in data.get("matches", []):
        fixtures.append({
            "home_team": map_team_name(match["homeTeam"]["name"]),
            "away_team": map_team_name(match["awayTeam"]["name"]),
            "match_date": match["utcDate"][:10],
            "matchweek": match["matchday"],
        })

    return fixtures, date_from, date_to