from numba import jit

from coding_challenges.algo.sorts.sort_utils import partition


@jit(nopython=True, nogil=True, fastmath=True)
def qsort(arr, first, last):
    if first == last or first < 0 or last >= len(arr):
        return

    pivot = (arr[first] + arr[last]) / 2
    middle_index = partition(arr, first, last, pivot)

    qsort(arr, first, middle_index - 1)
    qsort(arr, middle_index, last)


if __name__ == "__main__":
    arr = [5, 1, 6, 2, 7, 3, 8, 3, 7, 2]
    qsort(arr, 0, len(arr) - 1)
    print(arr)
