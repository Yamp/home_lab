import numpy as np

# TODO: recursive matrix multiplication
# медианы нужно выгребать и класть рядом

# TODO: cache-oblivious BST (binary search tree)


def extend_with_infs(arr):
    l = len(arr)
    r = 5 - (l % 5 or 5)

    for i in range(r):
        arr += [np.inf]


def sort_fifth():
    pass

def median_median(arr):
    extend_with_infs(arr)
