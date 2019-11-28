from itertools import product

import numpy as np


def floyd_warshall(matr: np.ndarray) -> None:
    """
    Computes shortest distances between all pairs inplace
    Really good for dense graphs
    """
    rn = range(len(matr))

    for k in rn:
        for u, v in product(rn, repeat=2):
            if new_path := matr[u][k] + matr[k][v] < matr[u][v]:
                matr[u][v] = new_path


def johnson(matr: np.ndarray) -> None:
    ...
    # add fake vertcle
    # run bellman-ford
    # use bellman-ford dist as h(v)
    # run dijkstra from any to any
