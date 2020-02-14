import math
from typing import Optional


def _kth_bit(n: int, k: int) -> int:
    return n >> k & 1


def _first_k_bits(n: int, k: int) -> int:
    return n - (n >> k << k)


def _last_k_bits(n: int, k: int, total_bits: int) -> int:
    return n >> (total_bits - k)


class XFastTrieNode:
    def __init__(self):
        self.layers = []

        self.common_prefix = None

        self.left: Optional['XFastTrieNode'] = None
        self.right: Optional['XFastTrieNode'] = None

        self.descendant: Optional['XFastTrieNode'] = None
        self.parent: Optional['XFastTrieNode'] = None

    def find(self, n: int):
        return self.layers[n]

    def insert(self, n, level):
        ...


class XFastTrieLeafNode(XFastTrieNode):
    def __init__(self):
        super().__init__()
        self.next: Optional['XFastTrieLeafNode'] = None
        self.prev: Optional['XFastTrieLeafNode'] = None


class XFastTrie:
    def __init__(self):
        self.layers = []

    def find(self, n: int):
        return self.layers[-1][n]

    def successor(self, n: int):
        node = self._bin_search(n)
        if isinstance(node, XFastTrieLeafNode):
            return node.next

        if isinstance(node.right, XFastTrieLeafNode):
            return node.right

        # TODO:

    def insert(self):
        ...

    def _bin_search(self, n: int):
        total_bits = int(math.ceil(math.log2(n)))
        last = total_bits - 1
        first = 0

        while first != last:
            middle = (first + last) // 2
            bits = _first_k_bits(n, k=middle)
            if bits in self.layers[middle]:
                first = middle
            else:
                last = middle

        return self.layers[first][bits]
