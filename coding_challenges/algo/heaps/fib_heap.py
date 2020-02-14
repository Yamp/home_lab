from typing import Optional


class FibonacciHeapNode:
    def __init__(self, key: int):
        self.key: int = key
        self.parent: Optional[FibonacciHeapNode] = None
        self.child: FibonacciHeapNode = None
        self.left: FibonacciHeapNode = None
        self.right: FibonacciHeapNode = None

        self.degree = None
        self.mark = None


class FibonacciHeap:
    def __init__(self):
        self.size: int = 0
        self.min: FibonacciHeapNode = None

    def insert(self, key: int):
        new_node = FibonacciHeapNode(key)
        if self.size == 0:
            self._add_first_element(new_node)
        else:
            min.right
            # TODO:

        new_node.parent = None  # ?
        self.size += 1

    def get_min(self):
        return self.min.key

    def merge(self, other: 'FibonacciHeap'):
        if other.size == 0:
            return

        if self.size == 0:
            self.size = other.size
            self.min = other.min
        else:
            self._merge_lists(other)
            self.size += other.size

        if self.min and other.min and self.min.key > other.min.key:
            self.min = other.min

    def _merge_lists(self, other: 'FibonacciHeap'):
        self.min.right = other.min
        other.min.left = self.min

        self.min.left = other.min.left
        other.min.right = self
        # TODO: union lists


        self.min

    def _add_first_element(self, node: FibonacciHeapNode):
        self.min = node.left = node.right = node
