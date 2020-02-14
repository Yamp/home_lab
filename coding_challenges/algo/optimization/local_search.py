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

    @abc.abstractmethod
    def best_neighbor(self):
        """ Лучший сосед, который будет использоваться в дальнейшем """
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
    # TODO: add reheat
    current = curr_min = initial_point
    for i in range(max_iter):
        candidate = current.mutate()

        if np.random.rand() < acceptance_proba(curr_min.energy(), candidate.energy(), get_temp(i / max_iter)):
            current = candidate
            if candidate.energy() < curr_min.energy():
                curr_min = candidate

    return curr_min


def hill_climbing(initial_point, max_iter=10 ** 5, max_stagnation=100):
    stagnation = 0  # количество итераций без улучшения
    curr_min = initial_point  # текущий минимум

    for i in range(max_iter):
        candidate = curr_min.mutate()

        if curr_min.objective() > candidate.objective():
            curr_min, stagnation = candidate, 0
        elif stagnation := stagnation + 1 > max_stagnation:  # заканчиваем, если мы в стогнации
            break

    return curr_min


def tabu_search(
        initial_point,
        max_iter=10 ** 5,
        max_stagnation=1000,
        tabu_size=100
):
    # при стогнации можно увеличивать табу лист
    # можно хранить не полные состояния а мутации
    # или по-другому хранить пройденные состояния
    stagnation = 0  # количество итераций без улучшения
    curr_min = initial_point  # текущий минимум
    tabu_list = []

    for i in range(max_iter):
        candidate = curr_min.mutate()  # вариация как в hill_climbing будет более осмыслена

        if curr_min.objective() > candidate.objective() and candidate not in tabu_list:
            curr_min, stagnation = candidate, 0
            tabu_list.pop()
            tabu_list = [candidate] + tabu_list
        elif stagnation := stagnation + 1 > max_stagnation:  # заканчиваем, если мы в стогнации
            break

    return curr_min


def iterative_search_optimizer(
        initial_point_generator: Callable,
        optimizer: Callable,
        max_iter: int = 10 ** 5,
        max_stagnation: int = 100
):
    """
    Запускаем оптимизатор несколько раз из разных начальных точек и выбираем лучшее решение
    """
    curr_min = initial_point_generator()
    stagnation = 0

    for i in range(max_iter):
        initial_point = initial_point_generator()
        candidate = optimizer(initial_point)

        if curr_min.objective() > candidate.objective():
            curr_min, stagnation = candidate, 0
        elif stagnation := stagnation + 1 > max_stagnation:  # заканчиваем, если мы в стогнации
            break

    return curr_min


# TODO: fastest hill climbing (of all neighbours)
# TODO: выбор лучшего из n
# TODO: сэмплирование вариантов с вероятностями (гиббс?), принятие с вероятностями
# TODO: выбираем первого попавшегося
# TODO: случайно выбираем переменную, жадно выбираем место
# TODO: ждано выбираем и переменную и место куда ее нужно поставить
# TODO: no-degradation
# TODO: уменьшать не только количество, но и дальность скачков при приближении к концу


def evolution(population, max_iter=10 ** 5):
    population()


if __name__ == "__main__":
    initial = Func1dState(lambda x: x ** 3 - 2 * x ** 2 + 8 * x - 1)

    res = simulated_annealing(initial, max_iter=10 ** 4)
    print(res.state, res.energy())
