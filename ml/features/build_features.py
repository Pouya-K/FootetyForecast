import pandas as pd

df = pd.read_csv("ml/data/epl_combined.csv")
df["Date"] = pd.to_datetime(df["Date"])
elo_ratings = {}
features = []

K = 20

def get_elo(team):
    if team not in elo_ratings:
        elo_ratings[team] = 1500
    return elo_ratings[team]

def update_elo(home_team, away_team, result):
    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)

    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home

    if result == "H":
        actual_home, actual_away = 1, 0
    elif result == "D":
        actual_home, actual_away = 0.5, 0.5
    else: actual_home, actual_away = 0, 1

    elo_ratings[home_team] = home_elo + K * (actual_home - expected_home)
    elo_ratings[away_team] = away_elo + K * (actual_away - expected_away)


def get_team_stats(df, team, before_date, n = 5):
    team_matches = df[(df["Date"] < before_date) & ((df["HomeTeam"] == team) | (df["AwayTeam"] == team))].tail(n)

    goals_scored = []
    goals_conceded = []
    cards = []
    corners = []
    points = []

    for _, row in team_matches.iterrows():
        if row["HomeTeam"] == team:
            goals_scored.append(row["FTHG"])
            goals_conceded.append(row["FTAG"])
            corners.append(row["HC"])
            cards.append(row["home_cards"])
            points.append(3 if row["FTR"] == "H" else (1 if row["FTR"] == "D" else 0))
        else:
            goals_scored.append(row["FTAG"])
            goals_conceded.append(row["FTHG"])
            corners.append(row["AC"])
            cards.append(row["away_cards"])
            points.append(3 if row["FTR"] == "A" else (1 if row["FTR"] == "D" else 0))
    
    if len(goals_scored) == 0:
        return {
            "avg_goals_scored": 0,
            "avg_goals_conceded": 0,
            "avg_corners": 0,
            "avg_cards": 0,
            "avg_points": 0
        }
    
    return {
        "avg_goals_scored": sum(goals_scored) / len(goals_scored),
        "avg_goals_conceded": sum(goals_conceded) / len(goals_conceded),
        "avg_corners": sum(corners) / len(corners),
        "avg_cards": sum(cards) / len(cards),
        "avg_points": sum(points) / len(points)
    }

def get_rest_days(df, team, before_date):
    last_match = df[
        (df["Date"] < before_date) & 
        ((df["HomeTeam"] == team) | (df["AwayTeam"] == team))
    ]["Date"].max()
    
    if pd.notna(last_match):
        return (before_date - last_match).days
    else:
        return 7  # default if no previous match found

def get_venue_stats(df, team, before_date, venue="home", n=5):
    if venue == "home":
        matches = df[(df["Date"] < before_date) & (df["HomeTeam"] == team)].tail(n)
    else:
        matches = df[(df["Date"] < before_date) & (df["AwayTeam"] == team)].tail(n)

    if len(matches) == 0:
        return{
            "venue_avg_goals": 0,
            "venue_avg_corners": 0,
            "venue_avg_cards": 0,
            "venue_avg_points": 0
        }

    if venue == "home":
        return {
            "venue_avg_goals": matches["FTHG"].mean(),
            "venue_avg_corners": matches["HC"].mean(),
            "venue_avg_cards": matches["home_cards"].mean(),
            "venue_avg_points": matches["FTR"].apply(lambda x: 3 if x == "H" else (1 if x == "D" else 0)).mean()
        }
    
    return {
        "venue_avg_goals": matches["FTAG"].mean(),
        "venue_avg_corners": matches["AC"].mean(),
        "venue_avg_cards": matches["away_cards"].mean(),
        "venue_avg_points": matches["FTR"].apply(lambda x: 3 if x == "A" else (1 if x == "D" else 0)).mean()
    }

def get_h2h_stats(df, home_team, away_team, before_date, n=5):
    h2h = df[
        (df["Date"] < before_date) & 
        (
            ((df["HomeTeam"] == home_team) & (df["AwayTeam"] == away_team)) | 
            ((df["HomeTeam"] == away_team) & (df["AwayTeam"] == home_team))
        )
    ].tail(n)

    if len(h2h) == 0:
        return {
            "h2h_home_wins": 0, 
            "h2h_draws": 0, 
            "h2h_away_wins": 0, 
            "h2h_avg_goals": 0
        }
    
    home_wins = 0
    draws = 0
    away_wins = 0
    total_goals = []

    for _, row in h2h.iterrows():
        total_goals.append(row["FTHG"] + row["FTAG"])
        if row["HomeTeam"] == home_team:
            if row["FTR"] == "H":
                home_wins += 1
            elif row["FTR"] == "D":
                draws += 1
            else:
                away_wins += 1
        else:
            if row["FTR"] == "A":
                home_wins += 1
            elif row["FTR"] == "D":
                draws += 1
            else:
                away_wins += 1
    
    return {
        "h2h_home_wins": home_wins / len(h2h), 
        "h2h_draws": draws / len(h2h), 
        "h2h_away_wins": away_wins / len(h2h), 
        "h2h_avg_goals": sum(total_goals) / len(total_goals)
    }


for idx, row in df.iterrows():
    home_stats_5 = get_team_stats(df, row["HomeTeam"], row["Date"], n=5)
    away_stats_5 = get_team_stats(df, row["AwayTeam"], row["Date"], n=5)

    home_stats_10 = get_team_stats(df, row["HomeTeam"], row["Date"], n=10)
    away_stats_10 = get_team_stats(df, row["AwayTeam"], row["Date"], n=10)

    home_rest = get_rest_days(df, row["HomeTeam"], row["Date"])
    away_rest = get_rest_days(df, row["AwayTeam"], row["Date"])

    home_venue_5 = get_venue_stats(df, row["HomeTeam"], row["Date"], venue="home", n=5)
    away_venue_5 = get_venue_stats(df, row["AwayTeam"], row["Date"], venue="away", n=5)

    home_venue_10 = get_venue_stats(df, row["HomeTeam"], row["Date"], venue="home", n=10)
    away_venue_10 = get_venue_stats(df, row["AwayTeam"], row["Date"], venue="away", n=10)

    home_elo = get_elo(row["HomeTeam"])
    away_elo = get_elo(row["AwayTeam"])

    h2h = get_h2h_stats(df, row["HomeTeam"], row["AwayTeam"], row["Date"])

    feature_row = {
        "HomeTeam": row["HomeTeam"],
        "AwayTeam": row["AwayTeam"],
        "Date": row["Date"],

        "home_rest_days": home_rest,
        "away_rest_days": away_rest,

        "home_elo": home_elo,
        "away_elo": away_elo,
        "elo_diff": home_elo - away_elo,

        # head 2 head last 5 games
        "h2h_home_wins": h2h["h2h_home_wins"],
        "h2h_draws": h2h["h2h_draws"],
        "h2h_away_wins": h2h["h2h_away_wins"],
        "h2h_avg_goals": h2h["h2h_avg_goals"],

        # last 5 game averages
        "home_avg_goals_scored_5": home_stats_5["avg_goals_scored"],
        "home_avg_goals_conceded_5": home_stats_5["avg_goals_conceded"],
        "home_avg_corners_5": home_stats_5["avg_corners"],
        "home_avg_cards_5": home_stats_5["avg_cards"],
        "home_avg_points_5": home_stats_5["avg_points"],
        "away_avg_goals_scored_5": away_stats_5["avg_goals_scored"],
        "away_avg_goals_conceded_5": away_stats_5["avg_goals_conceded"],
        "away_avg_corners_5": away_stats_5["avg_corners"],
        "away_avg_cards_5": away_stats_5["avg_cards"],
        "away_avg_points_5": away_stats_5["avg_points"],

        # last 10 game averages
        "home_avg_goals_scored_10": home_stats_10["avg_goals_scored"],
        "home_avg_goals_conceded_10": home_stats_10["avg_goals_conceded"],
        "home_avg_corners_10": home_stats_10["avg_corners"],
        "home_avg_cards_10": home_stats_10["avg_cards"],
        "home_avg_points_10": home_stats_10["avg_points"],
        "away_avg_goals_scored_10": away_stats_10["avg_goals_scored"],
        "away_avg_goals_conceded_10": away_stats_10["avg_goals_conceded"],
        "away_avg_corners_10": away_stats_10["avg_corners"],
        "away_avg_cards_10": away_stats_10["avg_cards"],
        "away_avg_points_10": away_stats_10["avg_points"],

        # venue specific averages last 5 games
        "home_venue_avg_goals_5": home_venue_5["venue_avg_goals"],
        "home_venue_avg_corners_5": home_venue_5["venue_avg_corners"],
        "home_venue_avg_cards_5": home_venue_5["venue_avg_cards"],
        "home_venue_avg_points_5": home_venue_5["venue_avg_points"],
        "away_venue_avg_goals_5": away_venue_5["venue_avg_goals"],
        "away_venue_avg_corners_5": away_venue_5["venue_avg_corners"],
        "away_venue_avg_cards_5": away_venue_5["venue_avg_cards"],
        "away_venue_avg_points_5": away_venue_5["venue_avg_points"],

        # venue specific averages last 10 games
        "home_venue_avg_goals_10": home_venue_10["venue_avg_goals"],
        "home_venue_avg_corners_10": home_venue_10["venue_avg_corners"],
        "home_venue_avg_cards_10": home_venue_10["venue_avg_cards"],
        "home_venue_avg_points_10": home_venue_10["venue_avg_points"],
        "away_venue_avg_goals_10": away_venue_10["venue_avg_goals"],
        "away_venue_avg_corners_10": away_venue_10["venue_avg_corners"],
        "away_venue_avg_cards_10": away_venue_10["venue_avg_cards"],
        "away_venue_avg_points_10": away_venue_10["venue_avg_points"],

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
    update_elo(row["HomeTeam"], row["AwayTeam"], row["FTR"])

feature_df = pd.DataFrame(features)
feature_df.to_csv("ml/data/features.csv", index=False)
print(f"Build features for {len(feature_df)} matches")