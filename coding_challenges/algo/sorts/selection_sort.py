from copy import deepcopy
from typing import Any

import numpy as np

from coding_challenges.algo.sorts.sort_utils import find_min, shift_forward


def selection_sort(arr, first: int, last: int) -> Any:
    res = deepcopy(arr)

    for i in range(last - first + 1):
        res[i], ind = find_min(arr, first, last)
        arr[ind] = np.inf

    return res


def selection_sort_inplace(arr, first: int, last: int) -> None:
    for cur_pos in range(last - first + 1):
        min_, ind = find_min(arr, first + cur_pos, last)
        shift_forward(arr, cur_pos, ind - 1, 1)
        arr[cur_pos] = min_


if __name__ == "__main__":
    arr = [5, 1, 6, 2, 7, 3, 8, 3, 7, 2]
    selection_sort_inplace(arr, 0, len(arr) - 1)
    print(arr)

    arr = [5, 1, 6, 2, 7, 3, 8, 3, 7, 2]
    res = selection_sort(arr, 0, len(arr) - 1)
    print(res)
