from dataclasses import dataclass
from operator import itemgetter
from typing import Optional


@dataclass
class LeftistHeap:
    """
    Left rank >= right rank.
    Rank(null) = -1.
    Можно поворачивать

    # TODO: нужно обновлять везде ранги
    # TODO: нужно делать своп детей, если ранги нарушены
    """

    data: int
    rank: int = 0
    left: Optional['LeftistHeap'] = None
    right: Optional['LeftistHeap'] = None

    def calc_rank(self):
        ...

    def merge(self, other: Optional['LeftistHeap']):
        if other is None:
            return self

        small, big = sorted((self, other), key=itemgetter('data'))

        if small.right is not None:
            small.right = small.right.merge(big)
        else:
            small.right = big

        return small

    def min(self):
        return self.data

    def push(self, a: int) -> 'LeftistHeap':
        """ TODO: сделать вершиной в обертке """
        heap = LeftistHeap(a)
        return self.merge(heap)

    def pop(self) -> int:
        res = self.data
        new_self = self.left.merge(self.right)
