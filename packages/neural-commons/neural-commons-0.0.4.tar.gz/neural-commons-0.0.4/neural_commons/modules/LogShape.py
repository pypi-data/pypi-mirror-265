import logging

import torch
from torch import nn


class LogShape(nn.Module):
    def __init__(self, label: str):
        super().__init__()
        self.label = label

    def forward(self, x: torch.Tensor):
        logging.warning(f"{self.label}: {tuple(x.shape)}")
        return x
