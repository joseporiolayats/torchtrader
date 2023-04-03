"""
The test_moving_average() function asserts that the output of the
MovingAverage module matches the expected values for a given input.

Data:

values: A tensor of input values to compute the moving average.
window_size: An integer representing the window size to use for the
moving average.
First, the function instantiates a MovingAverage object with the given
window size.

Then, it computes the moving average values by passing in the data to the
object's forward() method.

Finally, it compares the computed values to the expected values and raises
 n assertion error
if they don't match.
"""

import pytest
import torch

from torchtrader.ta.ma import MovingAverage


@pytest.fixture
def moving_average():
    """
    Pytest fixture that creates a MovingAverage instance with window size 3.

    Returns:
        MovingAverage: A MovingAverage instance with window size 3.
    """
    return MovingAverage()


def test_initial_value(moving_average):
    """
    Test the initial value of the moving average.

    Args:
        moving_average (MovingAverage): A MovingAverage instance with
        window size 3.
    """
    assert moving_average.get() == torch.tensor(0.0)


def test_update(moving_average):
    """
    Test updating the moving average with many values.

    Args:
        moving_average (MovingAverage): A MovingAverage instance with
        window size 3.
    """
    moving_average.update(torch.tensor(2.0))
    assert moving_average.get() == torch.tensor(0.6667)

    moving_average.update(torch.tensor(4.0))
    assert moving_average.get() == torch.tensor(2.0)

    moving_average.update(torch.tensor(6.0))
    assert moving_average.get() == torch.tensor(4.0)


def test_reset(moving_average):
    """
    Test resetting the moving average to its initial value.

    Args:
        moving_average (MovingAverage): A MovingAverage instance with
        window size 3.
    """
    moving_average.update(torch.tensor(2.0))
    assert moving_average.get() == torch.tensor(0.6667)

    moving_average.reset()
    assert moving_average.get() == torch.tensor(0.0)


# %%
