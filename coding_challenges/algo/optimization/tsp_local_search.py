from itertools import combinations

from coding_challenges.algo.optimization.local_search import BasicLocalSearchState
import numpy as np


class TSPRoute(BasicLocalSearchState):
    def __init__(self, data: np.ndarray):
        super().__init__()
        self.data = data

    def mutate(self) -> 'TSPRoute':
        pass

    def objective(self):
        pass

    def swap(self, i, j):
        self.data[i, j] = self.data[j, i]

    def opt_2(self):
        for a, b in combinations(1, 2):
            ...
