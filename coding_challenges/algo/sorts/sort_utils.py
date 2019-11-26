from typing import Any

from numba import jit


@jit(nopython=True, nogil=True, fastmath=True)
def swap(arr, i: int, j: int) -> None:
    arr[i], arr[j] = arr[j], arr[i]


@jit(nopython=True, nogil=True, fastmath=True)
def partition(arr, first: int, last: int, pivot):
    while True:
        while arr[first] <= pivot:
            first += 1

        while arr[last] > pivot:
            last -= 1

        if first < last:
            swap(arr, first, last)
        else:
            break

    return first


@jit(nopython=True, nogil=True, fastmath=True)
def copy_array(
        src, dst,
        first: int, last: int,
        dst_first: int
) -> None:
    """ Copying part of the array to the other """
    for i in range(last - first + 1):
        dst[dst_first + i] = src[first + i]


@jit(nopython=True, nogil=True, fastmath=True)
def merge(
        src, dst,
        first1: int, last1: int,
        first2: int, last2: int,
        dst_first: int
) -> None:
    """ More or less optimized merge function """
    while True:
        if src[first1] < src[first2]:
            dst[dst_first] = src[first1]
            first1 += 1
            dst_first += 1

            if last1 < first1:
                copy_array(src, dst, first2, last2, dst_first)
                break
        else:
            dst[dst_first] = src[first2]
            first2 += 1
            dst_first += 1

            if last2 < first2:
                copy_array(src, dst, first1, last1, dst_first)
                break


@jit(nopython=True, parallel=True, nogil=True, fastmath=True)
def find_min(arr, first: int, last: int) -> Any:
    current_min, ind = arr[first], first

    for i in range(first + 1, last + 1):
        if arr[i] < current_min:
            current_min, ind = arr[i], i

    return current_min, ind


@jit(nopython=True, parallel=True, nogil=True, fastmath=True)
def shift_forward(arr, first: int, last: int, dist: int) -> None:
    for i in reversed(range(last - first + 1)):
        arr[first + dist + i] = arr[first + i]


@jit(nopython=True, parallel=True, nogil=True, fastmath=True)
def shift_backward(arr, first: int, last: int, dist: int) -> None:
    for i in range(last - first + 1):
        arr[first - dist + i] = arr[first + i]


def heap_merge(
        src, dst,
        firsts: int, lasts: int,
        dst_first: int
) -> None:
    pass
