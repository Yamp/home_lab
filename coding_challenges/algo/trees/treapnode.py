from dataclasses import dataclass
from typing import Optional, Iterable, Any, List

from coding_challenges.algo.trees.all_trees import BinaryNode


# TODO: Interval tree
# TODO: Priority search tree
# TODO: Early parser

@dataclass
class TreapElement:
    key: int
    priority: int
    value: Any = None


class TreapNode(BinaryNode):
    def __init__(self):
        super().__init__()
        self.priority = None

    def from_element(self, e: TreapElement):
        self.key = e.key
        self.priority = e.priority
        self.value = e.value
        return self

    def initialize(self, **kwargs):
        if 'priority' in kwargs:
            self.priority = kwargs['priority']

        return super().initialize(**kwargs)

    def merge(self, other: Optional['TreapNode']):
        """
        Merges other tree to this.
        Suggests that all keys in self are less then keys in other.
        """
        if other is None:
            return self

        if self.priority > other.priority:
            self.right = self.right.merge(other)
            return self
        else:
            other.left = other.left.merge(self)
            return other

    def insert(self, e: TreapElement):
        new_node = TreapNode().from_element(e)

        candidate = self
        while e.priority > candidate.priority:
            if new_candidate := candidate.get_branch(e.key) is None:
                self.set_child(new_node, is_left=e.key < self.key)
                break
            else:
                candidate = new_candidate
        else:
            candidate.replace_by(new_node)
            left, right = candidate.split_by(e.key)
            new_node.initialize(left=left, right=right)

        return new_node

    def erase(self, key) -> bool:
        node = self.find_node(key)

        if node is None:
            return False

        if node.left is None or node.right is None:
            self.replace_by(None)
        elif node.left is None:
            self.replace_by(node.right.merge(node.right))
        else:
            self.replace_by(node.left.merge(node.left))

        return True

    def unite(self, other):
        ...  # TODO: treap unite

    def build_from_sorted(self, elements: Iterable[TreapElement]):
        elements = iter(elements)
        first = next(elements)
        self.from_element(first)

        # TODO: from bottom to top!

        current = self
        for candidate in elements:
            while current.priority > candidate.priority:
                if (next_ := current.right) is None:
                    current.right = candidate
                    break
                else:
                    current = next_
            else:  # current.priority < candidate.priority
                current.replace_by(candidate)
                candidate.left = current

    def build_tree_naive(self, elements: Iterable[TreapElement]):
        elements = iter(elements)
        first = next(elements)
        self.from_element(first)

        for e in elements:
            self.insert(e)

    def build_tree_fast(self, elements: List[TreapElement]):
        elements.sort(key=lambda e: e.key)
        self.build_from_sorted(elements)
