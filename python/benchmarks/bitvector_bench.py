from time import time

from BitVector import BitVector
import numpy as np
from typing import Tuple

from blist import blist


def generate_operations(tests: int, arr_size: int) -> Tuple[np.ndarray, np.ndarray]:
    actions = np.random.randint(low=0, high=2, size=tests, dtype=np.int8)
    indices = np.random.randint(low=0, high=arr_size-1, size=tests, dtype=np.int32)

    return actions, indices


def bench(struct, actions: np.ndarray, indices: np.ndarray, times: int):
    start = time()
    _res = 0

    for t in range(times):
        for i, o in zip(indices, actions):
            struct[i] = o
            # add, val = divmod(o, 2)
            # if add:
            #     struct[i] = val
            # else:
            #     _res = struct[i]

    return time() - start


def bench_all(tests: int, arr_size: int, times: int):
    actions, indices = generate_operations(tests, arr_size)

    bit_vector = BitVector(size=arr_size)
    bool_list = [False] * arr_size
    bool_np = np.zeros(arr_size, dtype=np.bool)
    bool_blist = blist([False] * arr_size)

    bool_blist = bench(bool_blist, actions, indices, times)
    bit_vector = bench(bit_vector, actions, indices, times)
    bool_list = bench(bool_list, actions, indices, times)
    bool_np = bench(bool_np, actions, indices, times)

    print(f'{tests=}, {arr_size=}, {times=} ||| {bit_vector=} {bool_np=} {bool_list=} {bool_blist=}')


if __name__ == "__main__":
    for arr_size in [10, 100, 1000, 10**4, 10**5, 10**6]:
        bench_all(arr_size=arr_size, tests=300, times=1000)
