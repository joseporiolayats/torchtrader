"""test_macd.py"""
import torch

from torchtrader.ta.macd import MACD


def test_macd_numerical():
    macd = MACD()
    data = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    short_period = 3
    long_period = 6
    signal_period = 4

    macd_line, signal_line, hist = macd(data, short_period, long_period, signal_period)

    expected_macd_line = torch.tensor(
        [0.0000, 0.0667, 0.2118, 0.3448, 0.4857, 0.6286, 0.7714, 0.9143, 1.0571, 1.2000]
    )
    expected_signal_line = torch.tensor(
        [0.0000, 0.0241, 0.0667, 0.1216, 0.1905, 0.2705, 0.3600, 0.4581, 0.5636, 0.6750]
    )
    expected_hist = torch.tensor(
        [0.0000, 0.0426, 0.1451, 0.2233, 0.2952, 0.3581, 0.4114, 0.4562, 0.4935, 0.5250]
    )

    assert torch.allclose(macd_line, expected_macd_line, atol=1e-4)
    assert torch.allclose(signal_line, expected_signal_line, atol=1e-4)
    assert torch.allclose(hist, expected_hist, atol=1e-4)


def test_macd_jit():
    macd = MACD()
    scripted_macd = torch.jit.script(macd)

    data = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    short_period = 3
    long_period = 6
    signal_period = 4

    macd_line, signal_line, hist = macd(data, short_period, long_period, signal_period)
    jit_macd_line, jit_signal_line, jit_hist = scripted_macd(
        data, short_period, long_period, signal_period
    )

    assert torch.allclose(macd_line, jit_macd_line, atol=1e-4)
    assert torch.allclose(signal_line, jit_signal_line, atol=1e-4)
    assert torch.allclose(hist, jit_hist, atol=1e-4)
