import math
from timeit import timeit
import numpy as np

from numba import float32, int32, jit, prange
import numba
numba.config.THREADING_LAYER = 'tbb'


def print_time(func):
    res = timeit(f"{func.__name__}(1000000)", globals=globals(), number=10000)
    print(f"{func.__name__} = {res}")


def sin_sum(n):
    return sum(math.sin(i) for i in range(n))


@jit(nopython=True, parallel=True, nogil=True, fastmath=True)
def sin_sum_cycle(n):
    res = 0.0
    for i in prange(0, n):
        res += math.sin(i)
    return res


for f in [
    # sin_sum,
    sin_sum_cycle,
]:
    print_time(f)
