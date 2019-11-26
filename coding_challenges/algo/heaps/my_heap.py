from typing import Tuple

import numpy as np
from attr import dataclass


class BinHeap:
    """
    Heap, returning minimum element
    """

    def __init__(self, size: int):
        self.size = size
        self.data = np.zeros(size, dtype='int')
        self.last = -1

    def from_array(self, data: np.ndarray):
        self.data = data
        self.size = self.data.shape[0]
        self.last = self.size - 1

        for i in range(self.last, -1, -1):
            self._sift_down(i)

    def empty(self):
        return self.last == -1

    def push(self, a: int):
        self.last += 1

        if self.last == self.size - 1:
            raise OverflowError()

        self.data[self.last] = a
        self._sift_up()

    def min(self):
        return self.data[0]

    def pop(self):
        res = self.min()

        self._swap(0, self.last)
        self.last -= 1
        self._sift_down()

        return res

    def decrease_key(self, i: int, new_key: int) -> None:
        assert self.data[i] >= new_key

        self.data[i] = new_key
        self._sift_up(i)

    def delete(self, i: int) -> None:
        self.decrease_key(i, np.iinfo(np.int16).min)
        self.pop()

    # ------------------------------ protected ------------------------------------------

    def _smallest_child(self, a):
        try:
            return min(self._children(a), key=lambda x: self.data[x])
        except ValueError:
            return None

    def _swap(self, a, b):
        self.data[a], self.data[b] = self.data[b], self.data[a]

    def _children(self, a: int) -> Tuple:
        if 2 * a + 1 > self.last:
            return ()
        elif 2 * a + 2 > self.last:
            return 2 * a + 1,
        else:
            return 2 * a + 1, 2 * a + 2

    def _parent(self, a: int):
        return (a - 1) // 2 if a != 0 else None

    def _sift_down(self, i: int = None):
        current_pos = i or 0
        child_pos = self._smallest_child(current_pos)

        if child_pos is None:
            return

        while self.data[child_pos] < self.data[current_pos]:
            self._swap(child_pos, current_pos)
            current_pos = child_pos
            child_pos = self._smallest_child(current_pos)

            if child_pos is None:
                return

    def _sift_up(self, a=None):
        current_pos = a or self.last
        parent = self._parent(current_pos)

        if parent is None:
            return

        while self.data[current_pos] < self.data[parent]:
            self._swap(parent, current_pos)
            current_pos = parent
            parent = self._parent(current_pos)

            if parent is None:
                return


class KHeap:
    """
    Heap, returning minimum element
    Can add persistent element handles
    """

    def __init__(self, size: int):
        self.size = size
        self.data = np.zeros(size, dtype='int')
        self.last = -1
        self.k = 5

    def from_array(self, data: np.ndarray):
        self.data = data
        self.size = self.data.shape[0]
        self.last = self.size - 1

        for i in range(self.last, -1, -1):
            self._sift_down(i)

    def empty(self):
        return self.last == -1

    def push(self, a: int):
        self.last += 1

        if self.last == self.size - 1:
            raise OverflowError()

        self.data[self.last] = a
        self._sift_up()

    def min(self):
        return self.data[0]

    def pop(self):
        res = self.min()

        self._swap(0, self.last)
        self.last -= 1
        self._sift_down()

        return res

    def decrease_key(self, i: int, new_key: int) -> None:
        assert self.data[i] >= new_key

        self.data[i] = new_key
        self._sift_up(i)

    def delete(self, i: int) -> None:
        self.decrease_key(i, np.iinfo(np.int16).min)
        self.pop()

    # ------------------------------ protected ------------------------------------------

    def _smallest_child(self, a):
        try:
            return min(self._children(a), key=lambda x: self.data[x])
        except ValueError:
            return None

    def _swap(self, a, b):
        self.data[a], self.data[b] = self.data[b], self.data[a]

    def _children(self, a: int) -> Tuple:
        return tuple(self.k * a + i for i in range(self.k) if self.k * a + i < self.last)

    def _parent(self, a: int):
        return (a - 1) // self.k if a != 0 else None

    def _sift_down(self, i: int = None):
        current_pos = i or 0
        child_pos = self._smallest_child(current_pos)

        if child_pos is None:
            return

        while self.data[child_pos] < self.data[current_pos]:
            self._swap(child_pos, current_pos)
            current_pos = child_pos
            child_pos = self._smallest_child(current_pos)

            if child_pos is None:
                return

    def _sift_up(self, a=None):
        current_pos = a or self.last
        parent = self._parent(current_pos)

        if parent is None:
            return

        while self.data[current_pos] < self.data[parent]:
            self._swap(parent, current_pos)
            current_pos = parent
            parent = self._parent(current_pos)

            if parent is None:
                return


if __name__ == "__main__":
    h = BinHeap(10)
    h.push(1)
    h.push(3)
    h.push(2)
    h.push(5)
    h.push(-1)
    h.pop()
    h.push(-2)
    h.push(7)
    h.push(4)
    h.push(6)

    while not h.empty():
        print(h.pop(), end=' ')
    print()

    h = BinHeap(10)
    arr = np.array([4, 6, 2, 4, 8, 1])
    h.from_array(arr)

    while not h.empty():
        print(h.pop(), end=' ')
    print()
