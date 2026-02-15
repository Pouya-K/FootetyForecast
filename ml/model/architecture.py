import torch
import torch.nn as nn 

class MatchPredictor(nn.Module):
    def __init__(self, input_size):
        super().__init__