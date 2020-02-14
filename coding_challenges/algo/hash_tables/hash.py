import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from random import random, randrange

from typing import Any, Optional, List, Iterable, Type, Mapping, Dict

from llist import sllist


# TODO: hash bucket

@dataclass
class HashElement:
    key: Any
    value: Any


def get_universal_hash(a: int, b: int):
    """
    0 < a < p - 1
    0 < b < p
    """
    p = 9223372036854775783  # big prime

    def hash_(key: Any):
        return ((a + 1) * hash(key) + b) % p

    return hash_


class BasicHashTable(ABC):
    def __init__(self, initial_size: int = 10):
        self.table_size: int = initial_size
        self.elem_num = 0
        self.table: List = [self.create_cell() for i in range(self.table_size)]

    def item(self, key):
        cell = self.table[self._index(key)]

        for e in cell:
            if e.key == key:
                return e

        return None

    def get(self, key: Any, default=None) -> Any:
        res = self.item(key)

        if res is not None:
            return res.value
        else:
            return default

    @abstractmethod
    def add(self, elem: HashElement) -> None:
        ...

    @abstractmethod
    def delete(self, key: Any) -> None:
        ...

    @abstractmethod
    def create_cell(self):
        ...

    def _resize(self):
        self.table_size *= 2
        print(f'resizing {self.table_size}')

        old_table = self.table
        self.table = [self.create_cell() for i in range(self.table_size)]

        self.elem_num = 0
        for cell in old_table:
            for e in cell:
                self.add(e)

    def load_factor(self):
        return self.elem_num / self.table_size

    def _index(self, key) -> int:
        return hash(key) % self.table_size


class ArrayHashTable(BasicHashTable):
    def create_cell(self):
        return []

    def add(self, elem: HashElement) -> None:
        if (e := self.item(elem.key)) is not None:
            e.value = elem.value
            return

        self.elem_num += 1
        self.table[self._index(elem.key)] += [elem]

        if self.load_factor() > 0.25:
            self._resize()

    def delete(self, key):
        arr = self.table[self._index(key)]
        for i, e in enumerate(arr):
            if e.key == key:
                del arr[i]
                self.elem_num -= 1


class ListHashTable(BasicHashTable):
    def create_cell(self):
        return sllist()

    def add(self, elem: HashElement) -> None:
        if (e := self.item(elem.key)) is not None:
            e.value = elem.value
            return

        self.elem_num += 1
        self.table[self._index(elem.key)].append(elem)

        if self.load_factor() > 0.25:
            self._resize()

    def delete(self, key):
        list_ = self.table[self._index(key)]
        node = list_.first

        while node is not None:
            if node.value.key == key:
                list_.remove(node)
                self.elem_num -= 1
                return
            node = node.next


class Tombstone:
    _instance: Optional['Tombstone'] = None

    def __new__(cls: Type['Tombstone']) -> 'Tombstone':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class BaseOpenAddressTable(BasicHashTable, ABC):
    def is_filled(self, i):
        return self.table[i] is not None

    def is_deleted(self, i):
        return self.table[i] is Tombstone()

    def create_cell(self):
        return None


class OpenAddressHashTable(BaseOpenAddressTable):
    def add(self, elem):
        if (e := self.item(elem.key)) is not None:
            e.value = elem.value
            return

        start = self._index(elem.key)
        for i in range(start, self.table_size):
            if not self.is_filled(i):
                self.table[i] = elem
                self.elem_num += 1
                break
        else:
            self._resize()
            self.add(elem)

    def delete(self, key):
        start = self._index(key)

        for i in range(start, self.table_size):
            elem = self.table[i]
            if not self.is_filled(i):
                return None

            if self.is_deleted(i):
                continue

            if elem.key == key:
                self.table[i] = Tombstone()
                return elem
        else:
            return None

    def item(self, key):
        start = self._index(key)

        for i in range(start, self.table_size):
            elem = self.table[i]
            if not self.is_filled(i):
                return None

            if self.is_deleted(i):
                continue

            if elem.key == key:
                return elem
        else:
            return None

    def _resize(self):
        self.table_size *= 2
        print(f'resizing {self.table_size}')

        old_table = self.table
        self.table = [self.create_cell() for i in range(self.table_size)]

        self.elem_num = 0
        for i, e in enumerate(old_table):
            if isinstance(e, HashElement):
                self.add(e)


class DoubleHashingTable(BaseOpenAddressTable):
    def __init__(self, initial_size=10):
        super().__init__(initial_size)
        a, b = random.randint(0, sys.maxsize), random.randint(0, sys.maxsize)
        self._hash2 = get_universal_hash(a, b)

    def add(self, elem):
        start = self._index(elem.key)
        hash2 = self._hash2(elem.key)

        for iter_num in range(start, self.table_size):
            i = (start + iter_num * hash2) % self.table_size
            if not self.is_filled(i):
                self.table[i] = elem
                break
        else:
            self._resize()
            self.add(elem)

    def delete(self, key):
        start = self._index(key)
        hash2 = self._hash2(key)

        for iter_num in range(self.table_size):
            i = (start + iter_num * hash2) % self.table_size
            elem = self.table[i]
            if not self.is_filled(i):
                return None

            if self.is_deleted(i):
                continue

            if elem.key == key:
                self.table[i] = Tombstone()
                return elem
        else:
            return None


class CuckooHashTable(BasicHashTable):
    def __init__(self):
        super().__init__()
        self.table2 = ...
        a, b = random.randint(0, sys.maxsize), random.randint(0, sys.maxsize)
        self._hash2 = get_universal_hash(a, b)

    def create_cell(self):
        return None

    def item(self, key: Any, default=None) -> Any:
        i1 = self._index(key)
        i2 = self._hash2(key) % self.table_size

        elems = self.table[i1], self.table2[i2]
        for elem in elems:
            if elem is not None and elem.key == key:
                return elem

        return default

    def add(self, elem: HashElement) -> None:
        cur_elem = elem
        for i in range(20):
            i1, i2 = self._hashes(cur_elem.key)
            # TODO: cuckoo

    def delete(self, key: Any) -> None:
        i1 = self._index(key)
        i2 = self._hash2(key) % self.table_size

        if (elem := self.table[i1]) is not None:
            if elem.key == key:
                del self.table[i1]

        if (elem := self.table2[i2]) is not None:
            if elem.key == key:
                del self.table2[i2]

    def _hashes(self, key):
        return self._index(key), self._hash2(key) % self.table_size


class SquaredPerfectHash(BasicHashTable):

    def add(self, elem: HashElement) -> None:
        i = self._index(elem.key)

        if self.table[i] is None:
            raise ValueError('Коллиция!')

        self.table[i] = elem

    def get(self, key: Any):
        i = self._index(key)
        return self.table[i]

    def delete(self, key) -> None:
        i = self._index(key)
        self.table[i] = None

    def create_cell(self):
        return None

    def build_table(self, keys: List[Any]):
        self.size = 2 * len(keys)


class PerfectHashTable(BasicHashTable):
    def build_table(self, keys: List[Any]):
        self.size = 2 * len(keys)
        sets: List = [defaultdict(list) for i in range(self.size)]

        for k in keys:
            sets[self._index(k)] += [k]

        for s in sets:
            ...

    def add(self, elem: HashElement) -> None:
        ...

    def delete(self, key: Any) -> None:
        ...

    def create_cell(self):
        ...


def test_hash_table(class_: Type[BasicHashTable]):
    print(f'Testing {class_.__name__}')
    dict_: Dict = {}
    my_dict = class_()

    for i in range(100000):
        if not i % 1000:
            print(i)
        op = randrange(2)
        key, value = randrange(0, 1000), randrange(0, 10 ** 4)

        assert my_dict.get(key, None) == dict_.get(key, None)

        if op == 0:
            dict_[key] = value
            my_dict.add(HashElement(key, value))
        elif op == 1:
            my_dict.delete(key)
            dict_.pop(key, None)

        a, b = my_dict.get(key, None), dict_.get(key, None)
        assert a == b, f'{a} != {b}(dict) {op=} {key=} {value=}, {i=}'


if __name__ == "__main__":
    test_hash_table(ArrayHashTable)
    test_hash_table(ListHashTable)
    test_hash_table(OpenAddressHashTable)
