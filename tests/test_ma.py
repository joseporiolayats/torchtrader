import torch

from torchtrader.ta.ma import MovingAverage

# Create a torch.jit.ScriptModule from the MovingAverage class
MovingAverageTorchScript = torch.jit.script(MovingAverage())


def test_moving_average():
    ma = MovingAverageTorchScript

    # Test initial state
    assert torch.isclose(ma.get(), torch.tensor(0.0))

    # Test with a single value
    ma.forward(torch.tensor(1.0), 3)
    assert torch.isclose(ma.get(), torch.tensor(1.0 / 3))

    # Test with two values
    ma.forward(torch.tensor(2.0), 3)
    assert torch.isclose(ma.get(), torch.tensor(1.0))

    # Test with three values
    ma.forward(torch.tensor(3.0), 3)
    assert torch.isclose(ma.get(), torch.tensor(2.0))

    # Test with four values (rolling)
    ma.forward(torch.tensor(4.0), 3)
    assert torch.isclose(ma.get(), torch.tensor(3.0))

    # Test with a different window_size
    ma.forward(torch.tensor(5.0), 2)
    assert torch.isclose(ma.get(), torch.tensor(6.0))
