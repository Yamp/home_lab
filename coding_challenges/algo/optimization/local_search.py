import abc
import math
from abc import ABC
from functools import lru_cache
from typing import Callable

import numpy as np


class BasicLocalSearchState(ABC):
    @abc.abstractmethod
    def __init__(self):
        ...

    @abc.abstractmethod
    def mutate(self) -> 'BasicLocalSearchState':
        ...

    @abc.abstractmethod
    def objective(self):
        """ We will minimize the objective """
        ...

    @lru_cache()
    def energy(self) -> float:
        """ We will minimize the energy """
        return self.objective()

    def fitness(self):
        """ We will maximize fitness """
        return -self.objective()


class Func1dState(BasicLocalSearchState):
    def __init__(self, func: Callable, state=0) -> None:
        super().__init__()
        Func1dState.func = func
        self.state = state

    def mutate(self) -> 'BasicLocalSearchState':
        self.state += np.random.normal(5)
        return Func1dState(Func1dState.func, self.state + np.random.normal(5))

    def objective(self):
        return Func1dState.func(self.state)


def acceptance_proba(current: float, next_: float, temp: float) -> float:
    if next_ < current:
        return 1.0

    arg = (next_ - current) / temp
    arg = min(arg, 1000)
    return math.e ** (-arg)


def get_temp(progress: float) -> float:
    return max(1e-4, 1 - progress) ** 2 * 10 ** 5


def simulated_annealing(initial_point, max_iter=10 ** 5):
    current = curr_min = initial_point
    for i in range(max_iter):
        candidate = current.mutate()

        if np.random.rand() < acceptance_proba(curr_min.energy(), candidate.energy(), get_temp(i / max_iter)):
            current = candidate
            if candidate.energy() < curr_min.energy():
                curr_min = candidate

    return curr_min


if __name__ == "__main__":
    initial = Func1dState(lambda x: x ** 3 - 2 * x ** 2 + 8 * x - 1)

    res = simulated_annealing(initial, max_iter=10 ** 4)
    print(res.state, res.energy())
