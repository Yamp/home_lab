import numpy as np


# TODO: add sparce matrices

class FenwickTree:

    def __init__(self, size):
        self.data = np.zeros(size)

    def f(self, x: int) -> int:
        """ Sets all tail 1 to 0 """
        return x & (x + 1)

    def h(self, x: int) -> int:
        """ Sets last zero to 1 """
        return x | (x + 1)

    def sum(self, r: int) -> int:
        res = 0
        while r > 0:
            res += self.data[r]
            r = self.f(r) - 1

        return res

    def build_tree(self, array):
        ...

    def inc(self, i: int, delta: int):
        ...
