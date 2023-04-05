import torch
from torch.jit import script

from torchtrader.ta.rsi import RSI


def test_rsi() -> None:
    torch.manual_seed(42)
    prices = torch.randn(100)
    scripted_rsi_calculator = script(RSI())
    window_size = 14
    scripted_rsi = scripted_rsi_calculator(prices, window_size)

    assert scripted_rsi.shape == (100 - window_size + 1,)
    assert (scripted_rsi >= 0).all() and (scripted_rsi <= 100).all()

    # Test for a simple constant price series (RSI should be NaN)
    constant_prices = torch.tensor([50.0] * 100)
    scripted_rsi_constant = scripted_rsi_calculator(
        constant_prices, window_size
    )

    assert torch.isnan(scripted_rsi_constant).all()

    # Test for a simple increasing price series (RSI should be 100)
    increasing_prices = torch.tensor(list(range(1, 101)))
    scripted_rsi_increasing = scripted_rsi_calculator(
        increasing_prices, window_size
    )

    assert torch.isclose(
        scripted_rsi_increasing, torch.tensor(100.0), atol=1e-6
    ).all()

    # Test for a simple decreasing price series (RSI should be 0)
    decreasing_prices = torch.tensor(list(range(100, 0, -1)))
    scripted_rsi_decreasing = scripted_rsi_calculator(
        decreasing_prices, window_size
    )

    assert torch.isclose(
        scripted_rsi_decreasing, torch.tensor(0.0), atol=1e-6
    ).all()


if __name__ == "__main__":
    test_rsi()
