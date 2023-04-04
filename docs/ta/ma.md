# Usage

 First the imports
```python
import torch
from torchtrader.ta.ma import MovingAverage
```

Then lets JIT it and create the window size of the Moving Average
```python
window_size = 3     # Parameter of MovingAverage
ma = torch.jit.script(MovingAverage(window_size))
data = torch.tensor(3)
```

Now lets call the function with the x value which is to be interpreted as
the input data, the actual value of the series.
```python
print(ma(data))
print(ma(data))
print(ma(data))
```

And the output should look as follows.
```
tensor([1.])
tensor([2.])
tensor([3.])
```
As it's been inputting a value of 3 for a window size of 3, the computed
output should be increasing or decreasing in n steps until it reaches the
input value.
Note that the steps number is window size.

::: torchtrader.ta.ma
