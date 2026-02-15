import pandas as pd

df = pd.read_csv("ml/data/epl_combined.csv")
df["Date"] = pd.to_datetime(df["Date"])

def get_team_stats(df, team, before_date, n = 5):
    team_matches = df[(df["Date"] < before_date) & ((df["HomeTeam"] == team) | (df["AwayTeam"] == team))].tail(n)

    goals_scored = []
    goals_conceded = []
    cards = []
    corners = []

    for _, row in team_matches.iterrows():
        if row["HomeTeam"] == team:
            goals_scored.append(row["FTHG"])
            goals_conceded.append(row["FTAG"])
            corners.append(row["HC"])
            cards.append(row["home_cards"])
        else:
            goals_scored.append(row["FTAG"])
            goals_conceded.append(row["FTHG"])
            corners.append(row["AC"])
            cards.append(row["away_cards"])
    
    if len(goals_scored) == 0:
        return {
            "avg_goals_scored": 0,
            "avg_goals_conceded": 0,
            "avg_corners": 0,
            "avg_cards": 0
        }
    
    return {
        "avg_goals_scored": sum(goals_scored) / len(goals_scored),
        "avg_goals_conceded": sum(goals_conceded) / len(goals_conceded),
        "avg_corners": sum(corners) / len(corners),
        "avg_cards": sum(cards)/len(cards)
    }

features = []

for idx, row in df.iterrows():
    home_stats = get_team_stats(df, row["HomeTeam"], row["Date"])
    away_stats = get_team_stats(df, row["AwayTeam"], row["Date"])

    feature_row = {
        "HomeTeam": row["HomeTeam"],
        "AwayTeam": row["AwayTeam"],
        "Date": row["Date"],
        # Home team features
        "home_avg_goals_scored": home_stats["avg_goals_scored"],
        "home_avg_goals_conceded": home_stats["avg_goals_conceded"],
        "home_avg_corners": home_stats["avg_corners"],
        "home_avg_cards": home_stats["avg_cards"],
        # Away team features
        "away_avg_goals_scored": away_stats["avg_goals_scored"],
        "away_avg_goals_conceded": away_stats["avg_goals_conceded"],
        "away_avg_corners": away_stats["avg_corners"],
        "away_avg_cards": away_stats["avg_cards"],
        # Targets (what the model will predict)
        "FTR": row["FTR"],
        "FTHG": row["FTHG"],
        "FTAG": row["FTAG"],
        "HC": row["HC"],
        "AC": row["AC"],
        "home_cards": row["home_cards"],
        "away_cards": row["away_cards"],
    }
    features.append(feature_row)

feature_df = pd.DataFrame(features)
feature_df.to_csv("ml/data/features.csv", index=False)
print(f"Build features for {len(feature_df)} matches")