"""
    The `test_ichimoku_cloud()` function asserts that the output of the
    `IchimokuCloud` module
    matches the expected values for a given input.

    Data:
    - high: A tensor of the highest prices for each period.
    - low: A tensor of the lowest prices for each period.
    - close: A tensor of closing prices for each period.

    First, the function instantiates an `IchimokuCloud` object with
     default parameters.

    Then, it computes the Ichimoku Cloud values by passing in the data to the
     object's `forward()` method.

    """
import pytest
import torch

from torchtrader.ta.ichimoku import IchimokuCloud


@pytest.fixture(scope="module")
def cloud():
    """
    Fix for pytest to check all the module
    :return:
    """
    return IchimokuCloud()


def test_ichimoku_cloud(cloud):
    """
    Tests the IchimokuCloud module with some given data.

    :return: None
    """
    # Create data
    high = torch.tensor([10.0, 11.0, 12.0, 13.0, 14.0, 15.0])
    low = torch.tensor([8.0, 9.0, 10.0, 11.0, 12.0, 13.0])
    close = torch.tensor([9.0, 10.0, 11.0, 12.0, 13.0, 14.0])

    # Compute the Ichimoku Cloud values
    conversion_line, base_line, span_a, span_b, chikou_span = cloud(high, low, close)

    assert isinstance(conversion_line, torch.Tensor)
    assert isinstance(base_line, torch.Tensor)
    assert isinstance(span_a, torch.Tensor)
    assert isinstance(span_b, torch.Tensor)
    assert isinstance(chikou_span, torch.Tensor)

    assert conversion_line.shape == high.shape
    assert base_line.shape == high.shape
    assert span_a.shape == high.shape
    assert span_b.shape == high.shape
    assert chikou_span.shape == close.shape
