import pandas as pd 
import torch
import torch.nn as nn 
from architecture import MatchPredictor

df = pd.read_csv("ml/data/features.csv")

feature_cols = [
    "home_avg_goals_scored", "home_avg_goals_conceded",
    "home_avg_corners", "home_avg_cards",
    "away_avg_goals_scored", "away_avg_goals_conceded",
    "away_avg_corners", "away_avg_cards",
]

X = df[feature_cols].values

fullTimeResult_map = {"H": 0, "D": 1, "A": 2}
y_wdl = df["FTR"].map(fullTimeResult_map).values

y_goals = df[["FTHG", "FTAG"]].values
y_corners = df[["HC", "AC"]].values
y_cards = df[["home_cards", "away_cards"]].values 

X_tensor = torch.tensor(X, dtype=torch.float32)
y_wdl_tensor = torch.tensor(y_wdl, dtype=torch.long)
y_goals_tensor = torch.tensor(y_goals, dtype=torch.float32)
y_corners_tensor = torch.tensor(y_corners, dtype=torch.float32)
y_cards_tensor = torch.tensor(y_cards, dtype=torch.float32)

split = int(len(X_tensor) * 0.8)

X_train, X_val = X_tensor[:split], X_tensor[split:]
y_wdl_train, y_wdl_val = y_wdl