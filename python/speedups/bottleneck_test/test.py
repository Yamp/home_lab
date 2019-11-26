import numpy as np
import bottleneck as bn

a = np.array([1, 2, np.nan, 4, 5])

print(bn.nansum(a))
print(bn.move_median(a, window=2, min_count=1))
bn.bench()
bn.push()
