import math

from typing import Optional, List


class VEBTreeNode:
    def __init__(self, u: int):
        self.u: int = 2
        self.min: Optional[int] = None
        self.max: Optional[int] = None

        if u > 2:
            self.clusters: List[Optional['VEBTreeNode']] = [None] * self.high(u)
            self.summary = None  # VEB(self.high(self.u))

    def high(self, x):
        return int(x * self.u ** -0.5)

    def low(self, x):
        return int((x % math.ceil(self.u ** 0.5)))

    def check(self, x: int):
        if x == self.min or x == self.max:
            return True
        elif self.u > 2 and (cluster := self.clusters[self.high(x)]) is not None:
            return cluster.check(self.low(x))  # noqa
        else:
            return False

    def insert(self, n: int):
        if self.min is None:
            self.min = self.max = n
        elif self.min == self.max:
            if n < self.min:
                self.min = n
            else:
                self.max = n
        else:
            self.clusters[self.high(n)].insert(self.low(n))

    def delete(self, n: int):
        ...

    def successor(self, n: int) -> True:
        ...
