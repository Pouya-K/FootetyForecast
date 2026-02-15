import pandas as pd 
import torch
import torch.nn as nn 
from architecture import MatchPredictor
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
df = pd.read_csv(os.path.join(BASE_DIR, "ml", "data", "features.csv"))

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
y_wdl_train, y_wdl_val = y_wdl_tensor[:split], y_wdl_tensor[split:]
y_goals_train, y_goals_val = y_goals_tensor[:split], y_goals_tensor[split:]
y_corners_train, y_corners_val = y_corners_tensor[:split], y_corners_tensor[split:]
y_cards_train, y_cards_val = y_cards_tensor[:split], y_cards_tensor[split:]

model = MatchPredictor(input_size=8)

optimizer = torch.optim.AdamW(model.parameters(), lr = 0.001)

criterion_wdl = nn.CrossEntropyLoss()
criterion_regression = nn.MSELoss()

num_epochs = 100

for epoch in range(num_epochs):
    model.train()

    wdl_pred, goals_pred, corners_pred, cards_pred = model(X_train)

    loss_wdl = criterion_wdl(wdl_pred, y_wdl_train)
    loss_goals = criterion_regression(goals_pred, y_goals_train)
    loss_corners = criterion_regression(corners_pred, y_corners_train)
    loss_cards = criterion_regression(cards_pred, y_cards_train)

    total_loss = loss_wdl + loss_goals + loss_corners + loss_cards

    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch + 1} / {num_epochs} | Loss: {total_loss.item():.4f}")

model.eval()

with torch.no_grad():
    wdl_pred, goals_pred, corners_pred, cards_pred = model(X_val)
    
    val_loss_wdl = criterion_wdl(wdl_pred, y_wdl_val)
    val_loss_goals = criterion_regression(goals_pred, y_goals_val)
    val_loss_corners = criterion_regression(corners_pred, y_corners_val)
    val_loss_cards = criterion_regression(cards_pred, y_cards_val)

    val_total_loss = val_loss_wdl + val_loss_goals + val_loss_corners + val_loss_cards

    wdl_class = wdl_pred.argmax(dim = 1)
    accuracy = (wdl_class == y_wdl_val).float().mean()

    print(f"\nValidation Loss: {val_total_loss.item():.4f}")
    print(f"WDL Accuracy: {accuracy.item():.2%}")

torch.save(
    model.state_dict(), 
    os.path.join(BASE_DIR, "ml", "models", "matchweek_v1.pt")
)
print("Model Saved!")