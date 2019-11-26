from coding_challenges.algo.sorts.sort_utils import swap


def bubble_sort(arr, first: int, last: int) -> None:
    changed = True

    while changed:
        changed = False

        for i in range(first, last):
            if arr[i] > arr[i + 1]:
                swap(arr, i, i+1)
                changed = True


if __name__ == "__main__":
    arr = [5, 1, 6, 2, 7, 3, 8, 3, 7, 2]
    bubble_sort(arr, 0, len(arr) - 1)
    print(arr)
