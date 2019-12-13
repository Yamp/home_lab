from typing import Optional

from coding_challenges.algo.trees.all_trees import BinaryNode

# TODO: Interval tree
# TODO: Priority search tree

class TreapNode(BinaryNode):
    def __init__(self):
        super().__init__()
        self.priority = None

    def initialize(self, **kwargs):
        if 'priority' in kwargs:
            self.priority = kwargs['priority']

        return super().initialize(**kwargs)

    def merge(self, other: Optional['TreapNode']):
        """ Suggesting that all keys in self are less then keys in other """
        if other is None:
            return self

        if self.priority > other.priority:
            self.right = self.right.merge(other)
            return self
        else:
            other.left = other.left.merge(self)
            return other

    def insert(self, key, priority, value=None):
        new_node = TreapNode().initialize(key=key, priority=priority, value=value)

        candidate = self
        while priority > candidate.priority:
            if new_candidate := candidate.get_branch(key) is None:
                self.set_child(new_node, is_left=key < self.key)
                break
            else:
                candidate = new_candidate
        else:
            candidate.replace_by(new_node)
            left, right = candidate.split_by(key)
            new_node.initialize(left=left, right=right)

        return new_node

    def erase(self, key) -> bool:
        node = self.find_node(key)

        if node is None:
            return False

        if node.left is None or node.right is None:
            self.replace_by(None)
        elif node.left is None:
            self.replace_by(node.left.merge(node.right))
        else:
            self.replace_by(node.right.merge(node.left))

        return True

    def unite(self, other):
        ...
