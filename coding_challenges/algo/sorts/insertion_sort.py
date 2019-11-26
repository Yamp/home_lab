from numba import jit

from coding_challenges.algo.sorts.sort_utils import swap


@jit(nopython=True, nogil=True, fastmath=True)
def insertion_sort(arr, first: int, last: int) -> None:
    for current in range(first + 1, last + 1):
        unsorted = current
        # sinking unsorted down
        while unsorted > first and arr[unsorted] < arr[unsorted - 1]:
            swap(arr, unsorted, unsorted - 1)
            unsorted -= 1


if __name__ == "__main__":
    arr = [5, 1, 6, 2, 7, 3, 8, 3, 7, 2]
    insertion_sort(arr, 0, len(arr) - 1)
    print(arr)
