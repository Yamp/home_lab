from random import getrandbits
from typing import Any, Optional, Type, List

# TODO: consistent hashing
from coding_challenges.algo.structures.linked_list import LinkedListNode, LinkedList, LinkedListIterator


class Infinity:
    _instance: Optional['Infinity'] = None

    def __new__(cls: Type['Infinity']) -> 'Infinity':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return self is other


class NegInfinity:
    _instance: Optional['NegInfinity'] = None

    def __new__(cls: Type['NegInfinity']) -> 'NegInfinity':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

    def __le__(self, other):
        return True

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return self is other


class SkipList:
    def __init__(self):
        self.lists: List[LinkedList] = [
            self._create_list(),
            self._create_list(),
        ]

    def find_next(self, key) -> Any:
        # TODO: choose closest (lower or upper)
        next_list = self.lists[-1]
        while next_list is not self.lowest_list:
            next_list = self._successor_in_sorted(next_list, key).value

        return self._successor_in_sorted(next_list, key)

    def insert(self, key, value=None):
        next_ = self.find_next(key)
        new_node = LinkedListNode(key, value)
        next_.node.insert_before(new_node)

        if self._rand_bool():
            ...

    def _rand_bool(self) -> bool:
        return not getrandbits(1)  # dirty hack for performance. Random is slow

    def _successor_in_sorted(self, list_: LinkedList, key) -> LinkedListIterator:
        """ Returns closest next element """
        for i in list_:
            if i.key > key:
                return i

    def _create_list(self) -> 'LinkedList':
        res = LinkedList()
        res.push_back(NegInfinity())
        res.push_front(Infinity())

        return res


if __name__ == "__main__":
    ...
