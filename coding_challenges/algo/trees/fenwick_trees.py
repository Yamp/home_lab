import random
from typing import List

import numpy as np


# TODO: add sparce matrices
# TODO: дерево поиска с неявным ключем
# TODO: hyperloglog


class FenwickTree:
    # при индексации с единицы получаем длину отрезка — максимальную степень двойки, которая делит к


    def __init__(self, size):
        self.data = np.zeros(size, dtype=np.int32)

    def __len__(self) -> int:
        return len(self.data)

    def f(self, x: int) -> int:
        """ Sets all tail 1 to 0 """
        return x & (x + 1)

    def h(self, x: int) -> int:
        """ Sets last zero to 1 """
        return x | (x + 1)

    def sum(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.data[i]
            i -= -i & i
            # i = self.f(i) - 1

        return res

    def segm_sum(self, i: int, j: int) -> int:
        if i >= j:
            return 0
        return -self.sum(i) + self.sum(j)

    def inc(self, i: int, delta: int):
        i += 1
        while i < len(self):
            self.data[i] += delta
            i += -i & i
            # i = h(i)

    def build_tree(self, array):
        ...


class NonCommutativeFenwickTree:
    """
    It's all done in multiplicative fashion
    Won't work if it has zero elements
    """

    def __init__(self, size):
        self.data: List[str] = [''] * size

    def __len__(self) -> int:
        return len(self.data)

    def sum(self, i: int) -> str:
        res = ''  # neutral element
        while i > 0:
            res += self.data[i]
            i -= -i & i

        return res

    def segm_sum(self, i: int, j: int):
        str_i = self.sum(i)
        str_j = self.sum(j)

        return str_j[len(str_i):]  # str_i^-1 * str_j

    def inc(self, i: int, delta: int):
        i += 1
        j = i
        while j < len(self):
            str_ij = self.segm_sum(i, j)
            str_j = self.data[j]
            self.data[j] = str_j[:len(str_ij)] + delta + str_ij

            j += -j & j


def test_fenwick_tree():
    SIZE = 1000
    tree = FenwickTree(SIZE)
    arr = [0] * SIZE

    for i in range(100000):
        op = random.choice(['inc', 'sum'])

        if op == 'inc':
            item = random.randrange(0, SIZE)
            delta = random.randrange(100)

            arr[item] += delta
            tree.inc(item, delta)
        else:
            a, b = random.randrange(0, SIZE), random.randrange(1, SIZE)
            assert sum(arr[a:b]) == tree.segm_sum(a, b), (f'{a, b, i=}, '
                                                          f'{sum(arr[a:b])=}, '
                                                          f'{tree.segm_sum(a, b)=} '
                                                          f'{arr=}')


def test_non_commutative_fenwik_tree():
    SIZE = 1000
    tree = NonCommutativeFenwickTree(SIZE)
    arr = [0] * SIZE

    for i in range(100000):
        op = random.choice(['inc', 'sum'])

        if op == 'inc':
            item = random.randrange(0, SIZE)
            delta = random.randrange(100)

            arr[item] += delta
            tree.inc(item, delta)
        else:
            a, b = random.randrange(0, SIZE), random.randrange(1, SIZE)
            assert sum(arr[a:b]) == tree.segm_sum(a, b), (f'{a, b, i=}, '
                                                          f'{sum(arr[a:b])=}, '
                                                          f'{tree.segm_sum(a, b)=} '
                                                          f'{arr=}')


if __name__ == "__main__":
    test_fenwick_tree()
