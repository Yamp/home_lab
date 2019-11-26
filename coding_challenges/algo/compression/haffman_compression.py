from dataclasses import dataclass
from operator import attrgetter
from typing import Optional, List, Tuple

import numpy as np
from iteration_utilities._iteration_utilities import argmax


def calc_frequencies(data: bytes) -> np.ndarray:
    freqs = np.zeros(256)

    for d in data:
        freqs[d] += 1

    return freqs


@dataclass
class Tree:
    zero: Optional['Tree']
    one: Optional['Tree']

    freq: int
    letters: List[int]


class PriorityQueue:
    def __init__(self, data, key):
        self.data = data
        self.key = key

    def pop(self):
        ind = argmax(self.data, key=self.key)
        m1 = self.data[ind]
        del self.data[ind]
        return m1

    def push(self, elem):
        self.data += [elem]


class BitsBuffer:

    def __init__(self, max_bytes=1000):
        self.data: np.array = np.zeros(max_bytes // 8, dtype='int64')
        self.first_free_bit: int = 0

        self.CELL_SIZE = 8

    def increment_pointer(self, bits: int) -> None:
        self.first_free_bit += bits

    def cell_num(self):
        return self.first_free_bit // self.CELL_SIZE

    def bit_num(self):
        return self.first_free_bit % self.CELL_SIZE

    def append_bits(self, bits: int, bits_num: int) -> Tuple[int, int]:
        can_add = self.bit_num() + bits_num - self.CELL_SIZE
        self.data |= bits >> self.bit_num()

        if can_add < 0:
            self.increment_pointer(bits_num)
            return 0, 0
        else:
            self.increment_pointer(can_add)
            return bits_num - can_add, bits << can_add

    # ------------------------------- test methods -------------------------------

    def append_bit(self, b: int) -> None:
        self.data |= b >> self.bit_num()
        self.increment_pointer(1)

    def append_str(self, bit_str: int) -> None:
        for bit in bit_str:
            b = str(bit)


def build_huffman_tree(freqs: np.ndarray):
    trees = [Tree(None, None, freq, [byte]) for byte, freq in enumerate(freqs)]
    trees_que = PriorityQueue(data=trees, key=attrgetter('freq'))

    while len(trees_que.data) != 1:
        m1 = trees.pop()
        m2 = trees.pop()
        new_tree = Tree(m1, m2, m1.freq + m2.freq, m1.letters + m2.letters)
        trees_que.push(new_tree)

    return trees


def build_encoding_table():
    table = {}

    # def tree_transfer():


def encode(data: bytes, tree: Tree):
    freqs = calc_frequencies(data)
    tree = build_huffman_tree(freqs)


