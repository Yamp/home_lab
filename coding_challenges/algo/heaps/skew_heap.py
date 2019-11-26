from dataclasses import dataclass
from typing import Optional


@dataclass
class SkewNode:
    data: int
    left: Optional['SkewNode'] = None
    right: Optional['SkewNode'] = None

    def swap_children(self):
        self.left, self.right = self.right, self.left

    def merge(self, other: 'SkewNode'):
        pass


@dataclass
class SkewHeap:
    node: SkewNode

    def merge(self):
        ...
