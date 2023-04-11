import torch
from torch import Tensor


class MovingAverage(torch.nn.Module):
    """
    Computes the moving average for a sequence of values.

    Args:
        window_size (int): The number of values to use in the moving average
            calculation.
    """

    def __init__(self, window_size: int = 3):
        """
        Initialize a new instance of MovingAverage.

        Args:
            window_size: The number of values to use in the moving average
                calculation.
        """
        super().__init__()
        self.window_size = window_size
        self.values = torch.zeros(self.window_size)

    def update(self, value: Tensor) -> None:
        """
        Update the moving average with a new value.

        Args:
            value: The new value to add to the moving average.
        """
        self.values = torch.roll(self.values, -1)
        self.values[-1] = value

    def get(self) -> Tensor:
        """
        Get the current moving average.

        Returns:
            The current value of the moving average.
        """
        return torch.div(torch.sum(self.values), self.window_size)

    def forward(self, value: Tensor, window_size: int) -> Tensor:
        """
        Compute the moving average with a new value and return the result.

        Args:
            value: The new value to add to the moving average.
            window_size: The number of values to use in the moving average
                calculation.

        Returns:
            The current value of the moving average.
        """
        self.window_size = window_size
        self.update(value)
        return self.get()
