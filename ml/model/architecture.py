import torch
import torch.nn as nn 

class MatchPredictor(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
        )

        self.wdl_head = nn.Linear(64, 3)
        self.goals_head = nn.Linear(64, 2)
        self.corners_head = nn.Linear(64, 2)
        self.cards_head = nn.Linear(64, 2)

        # Softplus for continuous non-negative outputs (smoother than ReLU,
        # avoids dead neurons that get stuck predicting 0)
        self.softplus = nn.Softplus()

    def forward(self, x):
        shared = self.shared(x)
        wdl = self.wdl_head(shared)
        goals = self.softplus(self.goals_head(shared))
        corners = self.softplus(self.corners_head(shared))
        cards = self.softplus(self.cards_head(shared))

        return wdl, goals, corners, cards