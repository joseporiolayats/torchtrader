from typing import Tuple

import torch
import torch.nn.functional as F
from torch import nn


class RSI(nn.Module):
    """
    The RSI class is a PyTorch implementation of the Relative Strength Index
    (RSI) indicator.

    ```mermaid
    graph LR
      A[Price Gains and Losses] --> B[Compute Average Gain and Loss]
      B --> C[Compute RS]
      C --> D[Compute RSI]
    ```
    """

    def __init__(self, window_size: int = 14):
        """
        Initializes the RSI class.

        Args:
            window_size (int): The size of the moving window to calculate
            average gain and loss. Defaults to 14.
        """
        super().__init__()
        self.window_size = window_size

    def forward(self, prices: torch.Tensor, window_size: int) -> torch.Tensor:
        """
        Computes the RSI values for the given price series and window size.

        Args:
            prices (torch.Tensor): The price series for which RSI values are
            to be calculated.
            window_size (int): The size of the moving window to calculate
            average gain and loss.

        Returns:
            torch.Tensor: The RSI values for the given price series and window
            size.
        """
        self.window_size = window_size
        gains_losses = prices[1:] - prices[:-1]
        gains, losses = self.compute_individual_gains_losses(gains_losses)
        avg_gain, avg_loss = self.compute_avg_gain_loss(gains, losses)
        rs = self.compute_rs(avg_gain, avg_loss)
        return self.compute_rsi(rs)

    def compute_individual_gains_losses(
        self, gains_losses: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes individual gains and losses from price changes.

        Args:
            gains_losses (torch.Tensor): The differences between consecutive
            prices.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: A tuple containing individual
            gains and losses.
        """
        gains = torch.where(gains_losses > 0, gains_losses, torch.tensor(0.0))
        losses = torch.abs(
            torch.where(gains_losses < 0, gains_losses, torch.tensor(0.0))
        )
        return gains, losses

    def compute_avg_gain_loss(
        self, gains: torch.Tensor, losses: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes the average gain and loss using a moving window.

        Args:
            gains (torch.Tensor): The individual gains of price changes.
            losses (torch.Tensor): The individual losses of price changes.

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: A tuple containing the average
            gain and loss.
        """
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
        """
        Computes the Relative Strength (RS) from the average gain and loss.

        Args:
            avg_gain (torch.Tensor): The     average gain of price changes.
        avg_loss (torch.Tensor): The average loss of price changes.

        Returns:
            torch.Tensor: The Relative Strength (RS) values.
        """
        return avg_gain / (avg_loss + 1e-10)

    def compute_rsi(self, rs: torch.Tensor) -> torch.Tensor:
        """
        Computes the RSI values from the Relative Strength (RS) values.

        Args:
            rs (torch.Tensor): The Relative Strength (RS) values.

        Returns:
            torch.Tensor: The RSI values.
        """
        return 100 - (100 / (1 + rs))
