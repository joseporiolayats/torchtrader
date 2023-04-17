"""
Ichimoku Cloud implemented in PyTorch with "Just In Time" (JIT) compilation
"""
import torch


class IchimokuCloud(torch.nn.Module):
    """
    A PyTorch implementation of the Ichimoku Cloud indicator. It computes
    five different lines:
    conversion line, baseline, span A, span B, and chikou span.

    Args:
        conversion_period (int): The conversion line period. Default as 9.
        base_period (int): The baseline period. Default as 26.
        span_b_period (int): The span B period. Default as 52.

    Attributes:
        conversion_period (int): The conversion line period.
        base_period (int): The baseline period.
        span_b_period (int): The span B period.

    """

    def __init__(self, conversion_period=9, base_period=26, span_b_period=52):
        super().__init__()
        self.conversion_period = conversion_period
        self.base_period = base_period
        self.span_b_period = span_b_period

    @staticmethod
    def kernel(x: torch.Tensor, period: int) -> torch.Tensor:
        """
        Applies the kernel calculation to a given tensor.

        Args:
            x (torch.Tensor): A tensor to transform.
            period (int): The kernel period.

        Returns:
            torch.Tensor: The transformed tensor.

        """
        k = (period - 1) / period
        return torch.cat(
            [
                torch.zeros(1, dtype=x.dtype, device=x.device),
                k * x[:-1] + (1 - k) * x[1:],
            ]
        )

    def forward(self, high: torch.Tensor, low: torch.Tensor, close: torch.Tensor) -> tuple:
        """
        Computes the Ichimoku Cloud indicator based on the high, low,
         and close price data.

        Args:
            high (torch.Tensor): A tensor containing the high-price data.
            low (torch.Tensor): A tensor containing the low-price data.
            close (torch.Tensor): A tensor containing the close price data.

        Returns:
            tuple: A tuple containing five tensors:
                   conversion line, baseline, span A, span B, and chikou span.

        """
        # Compute the conversion line
        conversion_line = (
            self.kernel(high, self.conversion_period) + self.kernel(low, self.conversion_period)
        ) / 2

        # Compute the baseline
        base_line = (self.kernel(high, self.base_period) + self.kernel(low, self.base_period)) / 2

        # Compute span A
        span_a = (conversion_line + base_line) / 2

        # Compute span B
        span_b = (self.kernel(high, self.span_b_period) + self.kernel(low, self.span_b_period)) / 2

        # Compute chikou span
        chikou_span = torch.roll(close, -self.base_period)

        return conversion_line, base_line, span_a, span_b, chikou_span
