from copy import deepcopy
from itertools import permutations
from timeit import timeit
from typing import Any

from coding_challenges.algo.sorts.insertion_sort import insertion_sort
from coding_challenges.algo.sorts.qsort import qsort
from coding_challenges.algo.sorts.sort_utils import copy_array, merge
import numpy as np

# TODO: m-way merge sort


def merge_bulks(src, dst, chunk_size: int, first: int, last: int) -> None:
    """
    Merging all chunks optimally
    We are leaving all residuals in the end
    """
    elem_num = last - first + 1
    regular_merges_num = elem_num // (chunk_size * 2)  # number of even full chunks

    # sorting all full chunks optimally
    first1 = first
    first2 = first1 + chunk_size
    last2 = first2 + chunk_size - 1

    for i in range(0, regular_merges_num):
        merge(
            src, dst,
            first1, first2 - 1,
            first2, last2,
            first1
        )

        first1 += 2 * chunk_size
        first2 += 2 * chunk_size
        last2 += 2 * chunk_size

    # This is not in the cycle to avoid redundant conditions in the cycle
    # All counters are already inplace
    if len(arr) % (chunk_size * 2) > chunk_size:  # If there are at least 2 chunks to merge
        merge(
            src, dst,
            first1, first2 - 1,
            first2, last,
            first1
        )
    else:
        copy_array(src, dst, first1, last, first1)


def sort_initial_chunks(arr, chunk_size: int, first: int, last: int) -> None:
    """
    Sorting initial chunks with insertion sort inplace
    """
    elem_num = last - first + 1
    regular_chunks_num = elem_num // chunk_size  # number of even full chunks

    # sorting all full chunks optimally
    first_sorted = first
    last_sorted = first_sorted + chunk_size - 1
    for i in range(0, regular_chunks_num):
        insertion_sort(arr, first_sorted, last_sorted)
        first_sorted += chunk_size
        last_sorted += chunk_size

    # sorting last chunk if it exists (to avid if in cycle)
    # first sorted is ok after cycle
    if elem_num % chunk_size != 0:
        last_sorted = last
        insertion_sort(arr, first_sorted, last_sorted)


def sort_with_buffer(
        arr, buffer,
        first: int, last: int,
        insertion_limit: int = 10
) -> Any:
    # recursion_base — insertion sort
    chunk_size = insertion_limit
    sort_initial_chunks(arr, chunk_size, first, last)
    res = buffer
    max_chunk = len(arr)

    while chunk_size <= max_chunk:
        merge_bulks(arr, res, chunk_size, first, last)
        chunk_size *= 2
        arr, res = res, arr

    return arr


def merge_sort(arr, first: int, last: int, insertion_limit=10) -> Any:
    buffer = deepcopy(arr)
    return sort_with_buffer(
        arr, buffer,
        first, last,
        insertion_limit
    )


if __name__ == "__main__":
    arr = np.random.rand(100000).tolist()

    for i in range(500, 1000, 10):
        test_arr = arr[:]
        # res = timeit(f"sorted(test_arr)", globals=globals(), number=100)  # 25 3.9130620070000006
        # res = timeit(f"test_arr.sort()", globals=globals(), number=100)  # 25 3.9130620070000006
        res = timeit(f"merge_sort(test_arr, 0, len(arr) - 1, insertion_limit=500)", globals=globals(), number=10)  # 25 3.9130620070000006
        # res = timeit(f"qsort(test_arr, 0, len(arr) - 1)", globals=globals(), number=10)  # 25 3.9130620070000006
        # res[]
        print(i, res)

    # for i in range(10, 500):
    #     arr = np.random.rand(i)
    #     res = merge_sort(arr.copy(), 0, len(arr) - 1, insertion_limit=3)
    #     print(np.allclose(res, sorted(arr)))

    # arr = [4, 3, 2, 1]
    # arr = [5, 1, 6, 2, 7, 3]
    # res = merge_sort(arr, 0, len(arr) - 1, insertion_limit=2)
    # print(res)
