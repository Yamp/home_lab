from dataclasses import dataclass
from itertools import product

import numpy as np


@dataclass
class GraphNode:
    path = 0


def dijsktra(self, start, end):
    heap = [(0, start)]  # cost from start node, end node
    visited = []
    while heap:
        (cost, u) = heapq.heappop(heap)
        if u in visited:
            continue
        visited.append(u)
        if u == end:
            return cost
        for v, c in self[u]:
            if v in visited:
                continue
            next = cost + c
            heapq.heappush(heap, (next, v))
    return (-1, -1)


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


def a_star(matrix: np.ndarray) -> None:
    ...


def johnson(matr: np.ndarray) -> None:
    ...
    # add fake vertcle
    # run bellman-ford
    # use bellman-ford dist as h(v)
    # run dijkstra from any to any


# TODO: hub system
# TODO: MLD, CH
# TODO: highway hierarchy
# TODO: meet in the middle dijkstra
# TODO: A*
