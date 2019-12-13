from dataclasses import dataclass
from itertools import product

import numpy as np

from coding_challenges.algo.heaps.python_heap import StdHeap


@dataclass
class GraphNode:
    index: int
    path: float


def dijsktra(matrix: np.ndarray, start: int, end: int) -> int:
    n = len(matrix)
    visited = [False] * n
    heap = StdHeap()

    def visit(node: GraphNode):
        visited[node.index] = True

        for v in range(n):
            if not visited[v] and matrix[node.index][v] > 0:
                heap.push(GraphNode(v, node.path + matrix[node.index][v]))

    visit(GraphNode(start, 0))
    while not heap.empty():
        node = heap.pop()
        if node.index != end:
            visit(node)
        else:
            return node.path


def floyd_warshall(matrix: np.ndarray) -> None:
    """
    Computes shortest distances between all pairs inplace
    Really good for dense graphs
    """
    rn = range(len(matrix))

    for k in rn:
        for u, v in product(rn, repeat=2):
            if new_path := matrix[u, k] + matrix[k, v] < matrix[u, v]:
                matrix[u, v] = new_path


def bellman_ford(matrix: np.ndarray, start: int):
    n, had_changes = len(matrix), False
    rn = range(n)
    prev_shortest, cur_shortest = np.full(n, np.inf), np.full(n, np.inf)
    prev_shortest[start] = cur_shortest[start] = 0

    for _ in rn:
        had_changes = False
        for u, v in product(rn, repeat=2):
            if cur_shortest[v] < (new := prev_shortest[u] + matrix[u, v]):
                cur_shortest[v] = new
                had_changes = True

    if had_changes:
        return None
    else:
        return cur_shortest


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
