"""
Moving Average implemented in PyTorch with "Just In Time" (JIT) compilation
"""

import torch


class MovingAverage(torch.nn.Module):
    """
    Computes the moving average for a sequence of values.

    Args:
        window_size (int): The number of values to use in the
        moving average calculation.
    """

    def __init__(self, window_size: int = 3):
        """
        Initialize a new instance of MovingAverage.

        Args:
            window_size: The number of values to use in the
            moving average calculation.
        """
        super().__init__()
        self.window_size = window_size
        self.values = torch.zeros(self.window_size)
        self.total = torch.zeros(1)

    def update(self, value: torch.Tensor) -> None:
        """
        Update the moving average with a new value.

        Args:
            value: The new value to add to the moving average.
        """
        oldest_value: torch.Tensor = self.values[0]
        self.total += value - oldest_value
        self.values = torch.roll(self.values, -1)
        self.values[-1] = value

    def get(self) -> torch.Tensor:
        """
        Get the current moving average.

        Returns:
            The current value of the moving average.
        """
        return self.total / self.window_size

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        """
        Compute the moving average with a new value and return the result.

        Args:
            value: The new value to add to the moving average.

        Returns:
            The current value of the moving average.
        """
        self.update(value)
        return self.get()
