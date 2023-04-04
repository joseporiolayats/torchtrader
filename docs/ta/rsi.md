# Usage

First the imports
```python
import torch
from torchtrader.ta.rsi import RSI
```

Then lets JIT it and create the window size of the Moving Average
```python
window_size = 10    # Parameter of MovingAverage
rsi = torch.jit.script(RSI(window_size))
data = torch.randn(1, 6, 50) + 100
```

Now lets call the function with the input data, the actual value of the series.
```python
print(rsi(data))
```

And the output should be a tensor of size 5 of non-zero values.


As it's been inputting a value of 3 for a window size of 3, the computed
output should be increasing or decreasing in n steps until it reaches the
input value.
Note that the steps number is window size.

::: torchtrader.ta.rsi
