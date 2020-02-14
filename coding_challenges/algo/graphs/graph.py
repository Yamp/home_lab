from typing import List

import numpy as np

from coding_challenges.algo.structures.array_queue import NumberArrayDeque


# TODO: euler cycle
# TODO: scc, briges, junctions

class Graph:
    def __init__(self):
        self.data = None

    def __len__(self):
        return len(self.data)

    def adjacent(self, v: int) -> np.array:
        return np.nonzero(self.data[v])[0]

    def iadjacent(self, v: int):
        for i in self.data[v]:
            yield i


class BFSVisitor:
    def __init__(self, graph: Graph):
        self.graph = graph

        self.queued = np.zeros(self.size, dtype='bool')
        self.queue = NumberArrayDeque(self.size)
        self.parent = np.zeros(self.size, dtype='int32')

    def drop_parents(self):
        self.parent = np.zeros(self.size, dtype='int32')

    def add2que(self, i: int, parent: int) -> None:
        self.queue.push_back(i)
        self.queued[i] = True
        self.parent[i] = parent

    def search(self, src: int, dst: int) -> bool:
        self.add2que(src, -1)

        if src == dst:
            self.add2que(src, src)
            return True

        while not self.queue.empty():
            current = self.queue.pop_front()

            for next_ in self.graph.adjacent(current):
                if next_ == dst:
                    self.add2que(next_, current)
                    return True

                if not self.queued[next_]:
                    self.add2que(next_, current)

        return False

    def get_path(self, src: int, dst: int) -> List[int]:
        if not self.search(src, dst):
            return []

        path = [dst]
        while path[-1] != src:
            last = path[-1]
            path.append(self.parent[last])

        return path[::-1]

    @property
    def size(self):
        return len(self.graph)


class MatrixGraph(Graph):
    def __init__(self, size: int):
        super().__init__()
        self.data = np.zeros((size, size), dtype='int32')


class FordFulkersonSolver:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.flows = np.zeros_like(self.graph.data)

        self.res_net = MatrixGraph(0)
        self.res_net.data = np.zeros_like(self.graph.data)  # residual network

    def eliminate_simple_loops(self):
        ...
        # TODO: disable self-loops
        # TODO: разбить узлы на кусочки

    def calc_path_flow(self, path: List[int]) -> int:
        return min(
            self.graph.data[path[i]][path[i + 1]]
            for i in range(len(path) - 1)
        )

    def update_flow(self, path: List[int]) -> None:
        """
        Flow(a -> b) = -Flow(b -> a)
        """
        flow = self.calc_path_flow(path)
        for i in range(len(path) - 1):
            self.flows[path[i]][path[i + 1]] += flow
            self.flows[path[i + 1]][path[i]] -= flow

    def calc_res_net(self):
        self.res_net.data = self.graph.data - self.flows  # todo: we can avoid extra memory

    def find_augmenting_path(self, src: int, dst: int) -> List[int]:
        return BFSVisitor(self.res_net).get_path(src, dst)

    def solve(self, src: int, dst: int) -> np.ndarray:
        while True:
            self.calc_res_net()
            path = self.find_augmenting_path(src, dst)

            if path:
                self.update_flow(path)
            else:
                break

        return self.flows


def junction_points(matrix: np.ndarray) -> np.ndarray:
    ...


def print_flows(flows: np.array):
    for i, row in enumerate(flows):
        for j in np.nonzero(row)[0]:
            # print('!', i, j, flows)
            v = flows[i][j]
            if v > 0:
                print(f'{i}->{j}={v}')


if __name__ == "__main__":
    graph = MatrixGraph(0)
    graph.data = np.array(
        [
            [0, 1000, 1000, 0],
            [0, 0, 1, 1000],
            [0, 0, 0, 1000],
            [0, 0, 0, 0],
        ]
    )

    res = FordFulkersonSolver(graph=graph).solve(0, 3)
    print_flows(res)
