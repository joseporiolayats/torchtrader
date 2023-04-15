import logging

import torch

from torchtrader.ta.ema import ExponentialMovingAverage

logging.basicConfig(level=logging.INFO)


def test_exponential_moving_average() -> None:
    ema_scripted = torch.jit.script(ExponentialMovingAverage(alpha=0.1))
    prices = torch.tensor([100.0, 101.0, 102.0, 103.0, 104.0], dtype=torch.float32)
    results = [
        100.0,
        100.0999984741211,
        100.28999328613281,
        100.56099700927734,
        100.90489959716797,
    ]
    test_results = []

    for price in prices:
        ema_value = ema_scripted(price, alpha=0.1)
        logging.info(f"EMA value: {ema_value}")
        assert isinstance(ema_value, torch.Tensor)
        test_results.append(float(ema_value))

    assert torch.isclose(torch.tensor(results), torch.tensor(test_results), atol=1e-6).all()


if __name__ == "__main__":
    test_exponential_moving_average()
