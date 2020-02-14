import sys
from copy import copy
from timeit import timeit
from typing import Any
import numpy as np

from coding_challenges.algo.sorts.sort_utils import find_max, find_min, partition


def selection_kth_statistics(arr, first: int, last: int, k: int) -> Any:
    arr = copy(arr)
    res = None

    if k - first > last - k:
        for i in range(k + 1):
            val, res = find_min(arr, first, last)
            arr[res] = sys.maxsize
    else:
        for i in range(k + 1):
            val, res = find_max(arr, first, last)
            arr[res] = sys.maxsize

    return res


def kth_statistics(arr, first, last, k):
    while first - last > 6:
        # pivot = (arr[first] + arr[last] + arr[(first + last) // 2]) / 3
        pivot = min(arr[(last + first) // 2], max(arr[first], arr[last]))
        middle_index = partition(arr, first, last, pivot)

        if k < middle_index:
            last = middle_index - 1
        else:
            first = middle_index
            k -= middle_index

    return selection_kth_statistics(arr, first, last, k)


def median(arr, first, last):
    return kth_statistics(arr, first, last, (first + last + 1) // 2)


def test_median():
    for i in range(10):
        size = 1000
        arr = np.random.randint(100, size=size)
        i = median(arr, 0, size - 1)
        assert arr[i] == sorted(arr)[size // 2]


if __name__ == "__main__":
    test_median()
    # t = timeit('test_median()', globals=globals(), number=100)
    # print(t)
