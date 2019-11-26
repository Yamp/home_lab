from typing import Any

import numpy as np


class ArrayDeque:
    def __init__(self, max_size: int):
        self.array = [None] * max_size

        self.first = 0
        self.next = 0

    def empty(self):
        return self.first == self.next

    def full(self):
        return self.next + 1 == self.first

    def push_back(self, elem: Any):
        self.array[self.next] = elem
        self.next = (self.next + 1) % len(self.array)

    def push_front(self, elem: Any):
        self.first = (self.first - 1) % len(self.array)
        self.array[self.first] = elem

    def pop_back(self) -> Any:
        self.next = (self.next - 1) % len(self.array)
        return self.array[self.next]

    def pop_front(self) -> Any:
        res = self.array[self.first]
        self.first = (self.first + 1) % len(self.array)
        return res


class NumberArrayDeque(ArrayDeque):
    def __init__(self, max_size: int):  # noqa
        self.array = np.zeros(max_size + 1, dtype=np.int16)

        self.first = 0
        self.next = 0
