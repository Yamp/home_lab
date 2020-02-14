import numpy as np


def extract_digit(num: int, i: int, base=10) -> int:
    return int(num // base ** (i - 1) % base)


def radix_sort(arr, max_len=None, base=10):
    max_len = max_len or max(len(str(num)) for num in arr)

    for i in range(max_len, -1, -1):
        buckets = [[] for _ in range(base)]
        for elem in arr:
            buckets[extract_digit(elem, max_len - i)] += [elem]

        arr[:] = sum(buckets, [])


if __name__ == "__main__":
    arr = np.random.randint(0, 999, 1000, dtype=np.int)
    radix_sort(arr, max_len=3, base=10)
    print(arr)
