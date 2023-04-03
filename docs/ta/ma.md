# Usage

 First the imports
```jupyterpython
import torch
from torchtrader.ta.ma import MovingAverage
```

Then let's JIT it and create the window size of the Moving Average
```jupyterpython
ma = torch.jit.script(MovingAverage(3))
x = torch.tensor(3)
```

Now let's call the function with the x value which is to be interpreted as
the input data, the actual value of the series.
```jupyterpython
print(ma(x))
print(ma(x))
print(ma(x))
```

And the output should be as follows.
```pycon
tensor([1.])
tensor([2.])
tensor([3.])
```
As we've been inputting a value of 3 for a window size of 3, the computed
output should be increasing or decreasing in n steps until it reaches the
input value.
Note that the steps number is window size.

::: torchtrader.ta.ma
