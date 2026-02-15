import torch
import torch.nn as nn 

class MatchPredictor(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
        )

        self.wdl_head = nn.Linear(32, 3)
        self.goals_head = nn.Linear(32, 2)
        self.corners_head = nn.Linear(32, 2)
        self.cards_head = nn.Linear(32, 2)

    def forward(self, x):
        shared = self.shared(x)
        wdl = torch.softmax(self.wdl_head(shared), dim=1)
        goals = torch.relu(self.goals_head(shared))
        corners = torch.relu(self.corners_head(shared))
        cards = torch.relu(self.cards_head(shared))

        return wdl, goals, corners, cards