from typing import Tuple

import torch
import torch.nn.functional as F
from torch import nn


class RSI(nn.Module):
    def __init__(self):
        super().__init__()
        self.window_size = 14

    def forward(self, prices: torch.Tensor, window_size: int) -> torch.Tensor:
        self.window_size = window_size
        gains_losses = prices[1:] - prices[:-1]
        gains, losses = self.compute_individual_gains_losses(gains_losses)
        avg_gain, avg_loss = self.compute_avg_gain_loss(gains, losses)
        rs = self.compute_rs(avg_gain, avg_loss)
        rsi = self.compute_rsi(rs)

        return rsi

    def compute_individual_gains_losses(
        self, gains_losses: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        gains = torch.where(gains_losses > 0, gains_losses, torch.tensor(0.0))
        losses = torch.abs(
            torch.where(gains_losses < 0, gains_losses, torch.tensor(0.0))
        )
        return gains, losses

    def compute_avg_gain_loss(
        self, gains: torch.Tensor, losses: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        gains_padded = F.pad(gains, (self.window_size - 1, 0))
        losses_padded = F.pad(losses, (self.window_size - 1, 0))

        avg_gain = F.avg_pool1d(
            gains_padded.unsqueeze(0).unsqueeze(0), self.window_size, stride=1
        ).squeeze()
        avg_loss = F.avg_pool1d(
            losses_padded.unsqueeze(0).unsqueeze(0), self.window_size, stride=1
        ).squeeze()

        return avg_gain, avg_loss

    def compute_rs(
        self, avg_gain: torch.Tensor, avg_loss: torch.Tensor
    ) -> torch.Tensor:
        return avg_gain / (avg_loss + 1e-10)

    def compute_rsi(self, rs: torch.Tensor) -> torch.Tensor:
        return 100 - (100 / (1 + rs))
