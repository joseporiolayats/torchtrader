""" MACD Indicator
"""
import torch
from torch import nn

from torchtrader.ta.ema import ExponentialMovingAverage


class MACD(nn.Module):
    """
    Moving Average Convergence Divergence (MACD) indicator implementation using PyTorch.

    ```mermaid
    graph LR
    data --> macd_line
    macd_line --> signal_line
    macd_line --> histogram
    signal_line --> histogram
    histogram --> forward_output
    ```

    """

    def __init__(self):
        super().__init__()
        self.ema = ExponentialMovingAverage()

    def macd_line(
        self, data: torch.Tensor, short_period: float, long_period: float
    ) -> torch.Tensor:
        """
        Calculate the MACD Line.

        ```mermaid
        graph LR
        data --> short_ema
        data --> long_ema
        short_ema --> macd_line_output
        long_ema --> macd_line_output
        ```

        Args:
            data (torch.Tensor): The input price data.
            short_period (float): The short EMA period.
            long_period (float): The long EMA period.

        Returns:
            torch.Tensor: The calculated MACD Line.
        """
        short_alpha = 2 / (short_period + 1)
        long_alpha = 2 / (long_period + 1)

        short_ema = torch.stack([self.ema(data[i], short_alpha) for i in range(len(data))])
        long_ema = torch.stack([self.ema(data[i], long_alpha) for i in range(len(data))])

        return short_ema - long_ema

    def signal_line(self, data: torch.Tensor, signal_period: float) -> torch.Tensor:
        """
        Calculate the Signal Line.


        Args:
            data (torch.Tensor): The input MACD Line data.
            signal_period (float): The signal EMA period.

        Returns:
            torch.Tensor: The calculated Signal Line.
        """
        signal_alpha = 2 / (signal_period + 1)
        return torch.stack([self.ema(data[i], signal_alpha) for i in range(len(data))])

    def histogram(self, macd_line: torch.Tensor, signal_line: torch.Tensor) -> torch.Tensor:
        """
        Calculate the Histogram.

        Args:
            macd_line (torch.Tensor): The input MACD Line data.
            signal_line (torch.Tensor): The input Signal Line data.

        Returns:
            torch.Tensor: The calculated Histogram.
        """
        return macd_line - signal_line

    def forward(
        self,
        data: torch.Tensor,
        short_period: float,
        long_period: float,
        signal_period: float,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Calculate the MACD Line, Signal Line, and Histogram for the given input data.

        ```mermaid
        graph LR
        data --> macd_line
        macd_line --> signal_line
        macd_line --> histogram
        signal_line --> histogram
        histogram --> forward_output
        ```

        Args:
            data (torch.Tensor): The input price data.
            short_period (float): The short EMA period.
            long_period (float): The long EMA period.
            signal_period (float): The signal EMA period.

        Returns:
            tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
            A tuple containing the calculated MACD Line, Signal Line,
            and Histogram.
        """
        macd_line = self.macd_line(data, short_period, long_period)
        signal_line = self.signal_line(macd_line, signal_period)
        hist = self.histogram(macd_line, signal_line)

        return macd_line, signal_line, hist
