import torch
import pandas as pd 
import os
import sys
import numpy as np
from sklearn.preprocessing import StandardScaler
from architecture import MatchPredictor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, "ml", "features"))
from build_features import get_team_stats, get_rest_days, get_venue_stats, get_h2h_stats, get_elo, elo_ratings, df

# Load trained model
model = MatchPredictor(input_size=45)
model.load_state_dict(torch.load(
    os.path.join(BASE_DIR, "ml", "models", "matchweek_v1.pt"),
    weights_only=True
))
model.eval()

features_df = pd.read_csv(os.path.join(BASE_DIR, "ml", "data", "features.csv"))
exclude_cols = ["HomeTeam", "AwayTeam", "Date", "FTR", "FTHG", "FTAG", "HC", "AC", "home_cards", "away_cards"]
feature_cols = [col for col in features_df.columns if col not in exclude_cols]
scaler = StandardScaler()
scaler.fit(features_df[feature_cols].values)

def predict_match(home_team, away_team):
    today = pd.Timestamp.now()

    home_stats_5 = get_team_stats(df, home_team, today, n=5)
    away_stats_5 = get_team_stats(df, away_team, today, n=5)

    home_stats_10 = get_team_stats(df, home_team, today, n=10)
    away_stats_10 = get_team_stats(df, away_team, today, n=10)

    home_rest = get_rest_days(df, home_team, today)
    away_rest = get_rest_days(df, away_team, today)

    home_venue_5 = get_venue_stats(df, home_team, today, venue="home", n=5)
    away_venue_5 = get_venue_stats(df, away_team, today, venue="away", n=5)

    home_venue_10 = get_venue_stats(df, home_team, today, venue="home", n=10)
    away_venue_10 = get_venue_stats(df, away_team, today, venue="away", n=10)

    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)

    h2h = get_h2h_stats(df, home_team, away_team, today)

    feature_values = [
        home_rest, away_rest,
        home_elo, away_elo, home_elo - away_elo,
        h2h["h2h_home_wins"], h2h["h2h_draws"], h2h["h2h_away_wins"], h2h["h2h_avg_goals"],
        home_stats_5["avg_goals_scored"], home_stats_5["avg_goals_conceded"],
        home_stats_5["avg_corners"], home_stats_5["avg_cards"], home_stats_5["avg_points"],
        away_stats_5["avg_goals_scored"], away_stats_5["avg_goals_conceded"],
        away_stats_5["avg_corners"], away_stats_5["avg_cards"], away_stats_5["avg_points"],
        home_stats_10["avg_goals_scored"], home_stats_10["avg_goals_conceded"],
        home_stats_10["avg_corners"], home_stats_10["avg_cards"], home_stats_10["avg_points"],
        away_stats_10["avg_goals_scored"], away_stats_10["avg_goals_conceded"],
        away_stats_10["avg_corners"], away_stats_10["avg_cards"], away_stats_10["avg_points"],
        home_venue_5["venue_avg_goals"], home_venue_5["venue_avg_corners"],
        home_venue_5["venue_avg_cards"], home_venue_5["venue_avg_points"],
        away_venue_5["venue_avg_goals"], away_venue_5["venue_avg_corners"],
        away_venue_5["venue_avg_cards"], away_venue_5["venue_avg_points"],
        home_venue_10["venue_avg_goals"], home_venue_10["venue_avg_corners"],
        home_venue_10["venue_avg_cards"], home_venue_10["venue_avg_points"],
        away_venue_10["venue_avg_goals"], away_venue_10["venue_avg_corners"],
        away_venue_10["venue_avg_cards"], away_venue_10["venue_avg_points"]
    ]

    X = scaler.transform([feature_values])
    X_tensor = torch.tensor(X, dtype=torch.float32)

    with torch.no_grad():
        wdl, goals, corners, cards = model(X_tensor)
    
    T = 1.3
    wdl = torch.softmax(wdl / T, dim=1)

    print(f"\n{'='*40}")
    print(f"{home_team} (H) vs {away_team} (A)")
    print(f"{'='*40}")
    print(f"  {home_team} Win: {wdl[0][0]:.1%}")
    print(f"  Draw: {wdl[0][1]:.1%}")
    print(f"  {away_team} Win: {wdl[0][2]:.1%}")
    print(f"  Goals: {goals[0][0]:.1f} - {goals[0][1]:.1f}")
    print(f"  Corners: {corners[0][0]:.1f} - {corners[0][1]:.1f}")
    print(f"  Cards: {cards[0][0]:.1f} - {cards[0][1]:.1f}")

if __name__ == "__main__":
    predict_match("Aston Villa", "Leeds")