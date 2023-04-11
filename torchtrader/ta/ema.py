import torch
from torch import Tensor


class ExponentialMovingAverage(torch.nn.Module):
    """
    Compute the Exponential Moving Average (EMA) of a sequence of input values.

    Args:
        alpha (float): The smoothing factor for the EMA computation.
    """

    def __init__(self, alpha: float = 0.1):
        super().__init__()
        self.alpha = alpha
        self.ema_value = torch.zeros(1)
        self.is_initialized = torch.tensor(False)

    def initialize(self, value: Tensor) -> None:
        """
        Initialize the EMA value with the first input value.

        Args:
            value (Tensor): The first input value to the EMA.
        """
        if not self.is_initialized:
            self.ema_value = value
            self.is_initialized = torch.tensor(True)

    def update(self, value: Tensor) -> None:
        """
        Update the EMA value with a new input value.

        Args:
            value (Tensor): The new input value to the EMA.
        """
        self.ema_value.mul_(1 - self.alpha).add_(self.alpha * value)

    def get(self) -> Tensor:
        """
        Get the current value of the EMA.

        Returns:
            Tensor: The current value of the EMA.
        """
        return self.ema_value

    def forward(self, value: Tensor, alpha: float) -> Tensor:
        """
        Compute the EMA value for a new input value.

        Args:
            value (Tensor): The new input value to the EMA.
            alpha (float): The smoothing factor for the EMA computation.

        Returns:
            Tensor: The new EMA value.
        """
        self.alpha = alpha
        self.update(value) if self.is_initialized else self.initialize(value)
        return self.get()
