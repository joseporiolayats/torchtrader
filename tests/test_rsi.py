"""
## RSI Test

This test checks the functionality of the RSI class.

### Fixture

#### `rsi`

Creates an instance of the RSI class with `window_size=5`.

### Test Function

#### `test_rsi(rsi)`

Tests the RSI class by computing the RSI values for a sample input tensor and
checking that the output values have the correct shape, type, and range.

#### Arguments

- `rsi` (RSI): An instance of the RSI class.

#### Returns

- `None`

"""


import pytest
import torch

from torchtrader.ta.rsi import RSI


@pytest.fixture
def rsi():
    """
    Fixture that creates an instance of the RSI class with window_size=5.

    Returns:
        RSI: An instance of the RSI class with window_size=5.
    """
    # Create an instance of the RSI class with window_size = 5
    return RSI(window_size=5)


def test_rsi(rsi):
    """
    Test function for the RSI class.

    Args:
        rsi (RSI): An instance of the RSI class.

    Returns:
        None
    """
    # Test the RSI class on a sample input
    prices = torch.tensor(
        [[10.0, 11.0, 12.0, 11.0, 10.0, 9.0, 8.0, 9.0, 10.0, 11.0]]
    )
    rsi_values = rsi(prices)

    # Check that the output has the correct shape and type
    assert isinstance(rsi_values, torch.Tensor)
    assert rsi_values.shape == prices.shape

    # Check that the output values are within the expected range
    assert (rsi_values >= 0).all() and (rsi_values <= 100).all()


# %%
