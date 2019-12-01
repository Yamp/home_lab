import numpy as np


# TODO: add sparce matrices

class FenwickTree:

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

    def inc(self, i: int, delta: int):
        while i < len(self):
            self.data[i] += delta
            i += -i & i
            # i = h(i)

    def build_tree(self, array):
        ...


if __name__ == "__main__":
    f = FenwickTree(100)
    f.inc(1, 20)
    f.inc(4, 4)
    print('0->1', f.sum(1))
    print('0->3', f.sum(3))
    print('0->4', f.sum(4))
    f.inc(2, -5)
    print('0->1', f.sum(1))
    print('0->3', f.sum(3))

    print(f.data)
