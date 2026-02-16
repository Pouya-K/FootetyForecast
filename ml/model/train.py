import pandas as pd 
import numpy as np
import torch
import torch.nn as nn 
from architecture import MatchPredictor
from sklearn.preprocessing import StandardScaler
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
df = pd.read_csv(os.path.join(BASE_DIR, "ml", "data", "features.csv"))

exclude_cols = ["HomeTeam", "AwayTeam", "Date", "FTR", "FTHG", "FTAG", "HC", "AC", "home_cards", "away_cards"]
feature_cols = [col for col in df.columns if col not in exclude_cols]

X = df[feature_cols].values
scaler = StandardScaler()
X = scaler.fit_transform(X)

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

model = MatchPredictor(input_size=len(feature_cols))

optimizer = torch.optim.AdamW(model.parameters(), lr = 0.0005)

criterion_wdl = nn.CrossEntropyLoss()

# Poisson NLL loss for count data (goals, corners, cards)
# This models the data as Poisson-distributed rather than normal,
# which is far more appropriate for goal/corner/card counts and
# avoids the mean-regression problem that MSE causes.
criterion_poisson = nn.PoissonNLLLoss(log_input=False, full=True)

# Keep MSE as a secondary metric for reporting
criterion_mse = nn.MSELoss()

num_epochs = 300

# Loss weights — upweight goals so the model focuses on getting scores right
W_WDL = 1.0
W_GOALS = 2.0
W_CORNERS = 0.5
W_CARDS = 0.5

# Print dataset stats for reference
print(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}")
print(f"Avg goals (train): Home {y_goals_train[:,0].mean():.2f}, Away {y_goals_train[:,1].mean():.2f}")

for epoch in range(num_epochs):
    model.train()

    wdl_pred, goals_pred, corners_pred, cards_pred = model(X_train)

    loss_wdl = criterion_wdl(wdl_pred, y_wdl_train)
    loss_goals = criterion_poisson(goals_pred, y_goals_train)
    loss_corners = criterion_poisson(corners_pred, y_corners_train)
    loss_cards = criterion_poisson(cards_pred, y_cards_train)

    total_loss = (W_WDL * loss_wdl + W_GOALS * loss_goals 
                  + W_CORNERS * loss_corners + W_CARDS * loss_cards)

    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch + 1} / {num_epochs} | Loss: {total_loss.item():.4f}"
              f" (wdl={loss_wdl.item():.3f}, goals={loss_goals.item():.3f})")

model.eval()

with torch.no_grad():
    wdl_pred, goals_pred, corners_pred, cards_pred = model(X_val)
    
    val_loss_wdl = criterion_wdl(wdl_pred, y_wdl_val)
    val_loss_goals = criterion_poisson(goals_pred, y_goals_val)
    val_loss_corners = criterion_poisson(corners_pred, y_corners_val)
    val_loss_cards = criterion_poisson(cards_pred, y_cards_val)

    val_total_loss = (W_WDL * val_loss_wdl + W_GOALS * val_loss_goals 
                      + W_CORNERS * val_loss_corners + W_CARDS * val_loss_cards)

    wdl_class = wdl_pred.argmax(dim = 1)
    accuracy = (wdl_class == y_wdl_val).float().mean()

    # Goal prediction diagnostics
    avg_pred_home = goals_pred[:, 0].mean().item()
    avg_pred_away = goals_pred[:, 1].mean().item()
    avg_actual_home = y_goals_val[:, 0].mean().item()
    avg_actual_away = y_goals_val[:, 1].mean().item()
    goals_mae = (goals_pred - y_goals_val).abs().mean().item()

    print(f"\nValidation Loss: {val_total_loss.item():.4f}")
    print(f"WDL Accuracy: {accuracy.item():.2%}")
    print(f"\nGoal Prediction Quality:")
    print(f"  Avg predicted: Home {avg_pred_home:.2f}, Away {avg_pred_away:.2f}")
    print(f"  Avg actual:    Home {avg_actual_home:.2f}, Away {avg_actual_away:.2f}")
    print(f"  Goals MAE:     {goals_mae:.3f}")

torch.save(
    model.state_dict(), 
    os.path.join(BASE_DIR, "ml", "models", "matchweek_v1.pt")
)
print("Model Saved!")