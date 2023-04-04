"""
RSI module implements the Relative Strength Index (RSI) indicator for PyTorch.

The RSI is as a momentum oscillator that measures the magnitude of recent
price
changes to evaluate overbought or oversold conditions in the price of an
asset. This module has a PyTorch implementation of RSI that takes in a
PyTorch tensor of prices and returns a PyTorch tensor of RSI values.

Example:
    To use this module, first create an instance of the `RSI` class with the
    desired window size:
    ```
    import torch
    from rsi import RSI

    prices = torch.tensor([[10.0, 11.0, 12.0, 11.0, 10.0, 9.0, 8.0, 9.0, 10.0,
                            11.0]])
    rsi = RSI(window_size=5)
    rsi_values = rsi(prices)
    ```

Classes:
    RSI: A class that implements the Relative Strength Index (RSI) indicator
    for PyTorch.

"""


from typing import Tuple

import torch
from torch import Tensor
from torch.nn.functional import avg_pool1d


class RSI(torch.nn.Module):
    def __init__(self, window_size: int):
        """
        Initializes the RSI module.

        Args:
            window_size (int): The size of the RSI window.
        """
        super().__init__()
        self.window_size = window_size

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Computes the RSI for a batch of time series data.

        Args:
            x (torch.Tensor): A batch of time series data in the shape
            (batch_size, sequence_length, num_features).

        Returns:
            torch.Tensor: The RSI values for each time step in the input data,
            in the shape (batch_size, sequence_length).
        """
        # Extract the closing prices from the input data
        close = self.get_close(x)

        # Compute the difference between consecutive closing prices
        delta = self.get_delta(close)

        # Separate the gains and losses from the price changes
        gain, loss = self.get_gain_loss(delta)

        # Compute the average gains and losses over the RSI window
        gain_avg, loss_avg = self.get_gain_loss_avg(gain, loss)

        # Compute the relative strength (RS) based on the average
        # gains and losses
        rs = self.get_rs(gain_avg, loss_avg)

        return self.get_rsi(rs)

    @staticmethod
    def get_close(x: torch.Tensor) -> torch.Tensor:
        """
        Extracts the closing prices from a batch of time series data.

        Args:
            x (torch.Tensor): A batch of time series data in the shape
            (batch_size, sequence_length, num_features).

        Returns:
            torch.Tensor: The closing prices for each time step in the input
            data, in the shape (batch_size, sequence_length).
        """
        # Extract the closing prices from the input data
        return x[:, -1]

    @staticmethod
    def get_delta(close: torch.Tensor) -> torch.Tensor:
        """
        Computes the difference between consecutive closing prices.

        Args:
            close (torch.Tensor): The closing prices for each time step in a
            batch of time series data.

        Returns:
            torch.Tensor: The price changes between consecutive time steps, in
            the shape (batch_size, sequence_length).
        """
        # Compute the difference between consecutive closing prices
        return close - torch.roll(close, 1, dims=1)

    @staticmethod
    def get_gain_loss(delta: torch.Tensor) -> Tuple[Tensor, Tensor]:
        """
        Separates gains and losses from price changes.

        Args:
            delta (torch.Tensor): The price changes between consecutive time
            steps, in the shape (batch_size, sequence_length).

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: The gains and losses for each
            time step, in the shape (batch_size, sequence_length).
        """
        # Separate gains and losses from price changes
        gain = torch.where(delta > 0, delta, torch.zeros_like(delta))
        loss = torch.where(delta < 0, -delta, torch.zeros_like(delta))
        return gain, loss

    def get_gain_loss_avg(
        self, gain: torch.Tensor, loss: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes the average gains and losses over the RSI window.

        Args:
            gain (torch.Tensor): The cumulative sum of gains for each time
            step, in the shape (batch_size, sequence_length).
            loss (torch.Tensor): The cumulative sum of losses for each time
             step, in the shape (batch_size, sequence_length).

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: The average gains and losses
            over the RSI window, each in the shape
            (batch_size, sequence_length).
        """
        # Compute the average gains and losses over the RSI window
        gain_avg = avg_pool1d(gain, kernel_size=self.window_size)
        loss_avg = avg_pool1d(loss, kernel_size=self.window_size)
        return gain_avg, loss_avg

    @staticmethod
    def get_rs(gain_avg: torch.Tensor, loss_avg: torch.Tensor) -> torch.Tensor:
        """
        Computes the relative strength (RS) based on the average gains
        and losses.

        Args:
            gain_avg (torch.Tensor): The average gains over the RSI window,
            in the shape (batch_size, sequence_length).
            loss_avg (torch.Tensor): The average losses over the RSI window,
            in the shape (batch_size, sequence_length).

        Returns:
            torch.Tensor: The relative strength values for each time step,
            in the shape (batch_size, sequence_length).
        """

        return torch.div(
            gain_avg,
            torch.where(torch.eq(loss_avg, 0), torch.tensor(1e-9), loss_avg),
        )

    @staticmethod
    def get_rsi(rs: torch.Tensor) -> torch.Tensor:
        """
        Computes the RSI based on the RS value.

        Args:
            rs (torch.Tensor): The relative strength values for each time step,
             in the shape (batch_size, sequence_length).

        Returns:
            torch.Tensor: The RSI values for each time step, in the shape
            (batch_size, sequence_length).
        """
        return 100 - 100 / (1 + rs)


# %%
