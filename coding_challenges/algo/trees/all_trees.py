from dataclasses import dataclass

from typing import List, Optional

# TODO: 2-3-trees, 2-3-4-tree, fenvik, segment-trees, B+, B*, R-tree, kd-tree
# TODO: Range trees, finger tree

@dataclass
class Node:
    """
    Rules:
    1) keys are gonna be sorted in ascending order
    2) < -> left >= -> right
    3) The root is a fake top node

    TODO: successor, predessor
    """
    parent: 'Node' = None
    children: List = None

    keys: List = None
    values: List = None

    def get_branch(self, k) -> 'Node':
        """
        Appropriate branch for search
        """
        for i, key in enumerate(self.keys):
            if k < key:
                return self.children[i]
        else:
            return self.children[-1]

    def nth_parent(self, n: int) -> 'Node':
        """
        nth parent or root
        """
        return self if n <= 0 else self.parent.nth_parent(n - 1)

    def get_branch_num(self, k) -> int:
        """
        Number of child for search
        """
        for i, key in enumerate(self.keys):
            if k < key:
                return self.children[i]
        else:
            return self.children[-1]

    def is_nth_child(self, n: int) -> bool:
        return (
                n in self.parent.children[n]
                and self is self.parent.children[n]
        )

    def is_leaf(self) -> bool:
        return not any(self.children)

    def is_fake_top(self) -> bool:
        return self.parent is None

    def is_root(self) -> bool:
        return self.parent.is_fake_top()

    def grandpa(self) -> 'Node':
        return self.nth_parent(2)

    def set_nth_child(self, child: 'Node', num: int) -> None:
        if child is not None:
            child.parent = self
        self.children[num] = child

    def found(self, k):
        return k in self.keys

    def _index(self, k) -> int:
        try:
            return self.children.index(k)
        except ValueError:
            return -1

    def find(self, k):
        if i := self._index(k) != -1:
            return self.values[i]
        elif self.is_leaf():
            return None
        return self.get_branch(k).find(k)

    def get_my_child_num(self):
        for i, c in enumerate(self.parent.children):
            if self is c:
                return i

    def add_new_value(self, k, v=None):
        new_node = self.__class__(keys=[k], values=[v], parent=self)
        self.children += [None]

        self.set_nth_child(new_node, num=len(children) - 1)  # noqa Type checker

    def usual_paste(self, k, v=None):
        next_branch = self.get_branch(k)
        if next_branch is None:
            new_node = self.__class__(keys=[k], values=[v], parent=self)
            self.set_nth_child(new_node, num=self.get_branch_num(k))  # noqa Type checker
            return new_node
        else:
            return next_branch.usual_paste(k, v)

    def replace_by(self, subtree: "BinaryNode"):
        num = self.get_my_child_num()
        self.parent.set_nth_child(subtree, num)


@dataclass
class BinaryNode(Node):

    def __init__(self):
        super(self.__class__).__init__(self)

        self.children = [None, None]
        self.parent: Optional['BinaryNode'] = None
        self.keys: List = [None]
        self.values: List = [None]

    @property
    def key(self):
        return self.keys[0]

    @key.setter
    def key(self, value):
        self.keys[0] = value

    @property
    def value(self):
        return self.values[0]

    @value.setter
    def value(self, val):
        self.values[0] = val

    @property
    def left(self) -> Optional['BinaryNode']:
        return self.children[0]

    @left.setter
    def left(self, value):
        self.children[0] = value

    @property
    def right(self):
        return self.children[1]

    @right.setter
    def right(self, value):
        self.children[1] = value

    def get_branch(self, k) -> 'BinaryNode':
        """
        The same but faster
        """
        return self.left if k < self.key else self.right

    def get_branch_name(self, k) -> str:
        return 'left' if k < self.key else 'right'

    def is_left_branch(self, k) -> bool:
        return k < self.key

    def is_left(self) -> bool:
        return self is self.parent.left

    def is_right(self) -> bool:
        return self is self.parent.right

    def get_child(self, is_left: bool) -> 'BinaryNode':
        return self.left if is_left else self.right

    def children(self) -> List['BinaryNode']:
        return [self.left, self.right]

    def grandpa(self) -> 'BinaryNode':
        """ It's here just for the type """
        return self.nth_parent(2)

    def brother(self) -> 'BinaryNode':
        return self.parent.left if self.is_right() else self.parent.right

    def uncle(self) -> 'BinaryNode':
        return self.parent.brother()

    def set_left(self, child: 'BinaryNode'):
        if child is not None:
            child.parent = self
        self.left = child

    def set_right(self, child: 'BinaryNode'):
        if child is not None:
            child.parent = self
        self.right = child

    def check_side(self, is_left: bool) -> bool:
        if is_left:
            return self.is_left()
        else:
            return self.is_right()

    def set_child(self, child: 'BinaryNode', is_left: bool):
        if is_left:
            self.set_left(child)
        else:
            self.set_right(child)

    def node_successor(self) -> 'BinaryNode':
        candidate_son = self
        while candidate_son.is_right():
            candidate_son = candidate_son.parent
        return candidate_son.parent

    def node_predecessor(self) -> 'BinaryNode':
        candidate_son = self
        while candidate_son.is_left():
            candidate_son = candidate_son.parent
        return candidate_son.parent

    def small_turn(self):
        is_right = self.is_left()  # TODO: wtf?
        is_left = not is_right

        b = self.get_child(is_right)
        c = b.get_child(is_left)

        self.replace_by(b)
        b.set_child(self, is_left)
        self.set_child(c, is_right)

    def big_turn(self):
        is_right = self.is_left()  # TODO: wtf?

        self.get_child(is_right).small_turn()
        self.small_turn()


@dataclass
class RedBlackBinaryNode(BinaryNode):
    def __init__(self):
        super().__init__()
        self.left: Optional['RedBlackBinaryNode'] = None
        self.right: Optional['RedBlackBinaryNode'] = None
        self.parent: Optional['RedBlackBinaryNode'] = None

        self._is_black: bool = True

    @staticmethod
    def check_black(node: 'RedBlackBinaryNode'):
        return node is None or node._is_black

    @staticmethod
    def check_red(node: 'RedBlackBinaryNode'):
        return not RedBlackBinaryNode.check_black(node)

    def make_black(self):
        self._is_black = True

    def make_red(self):
        self._is_black = False

    # case 5
    def rotate_to(self, left):
        p = self.parent
        g = self.grandpa()

        g.set_child(self.brother(), is_left=left)
        p.set_child(g, is_left=not left)
        g.replace_by(p)

    # case 4
    def small_rotate_to(self, left):
        p = self.parent
        p.set_child(self.get_child(is_left=left), is_left=not left)
        self.set_child(p, is_left=left)
        p.replace_by(self)

    def balance(self):
        if self.is_root():
            return self.make_black()
        elif self.check_red(self.parent):
            if self.check_red(self.uncle()):
                self.parent.make_black()
                self.uncle().make_black()
                self.grandpa().make_red()
                self.grandpa().balance()
            else:
                is_left_rotate = self.parent.is_left()
                if not self.parent.is_root() and self.is_left() != self.parent.is_left():  # 4 case
                    self.small_rotate_to(left=is_left_rotate)
                elif not self.parent.is_root():  # 5 case
                    self.rotate_to(left=is_left_rotate)

    def paste(self, k, v=None):
        pasted_node = self.usual_paste(k, v)
        pasted_node.make_red()
        pasted_node.balance()
        return pasted_node


@dataclass
class AVLBinaryNode(BinaryNode):
    height: int = 1

    def get_balance(self):
        if self.left.height - self.right.height:
            pass

    def paste(self, k, v=None):
        pasted_node = self.usual_paste(k, v)
        pasted_node.make_red()
        pasted_node.balance()
        return pasted_node


class SplayTree(BinaryNode):
    def zig(self):
        self.small_turn()

    def zigzig(self):
        self.grandpa().small_turn()
        self.parent.small_turn()

    def zigzag(self):
        self.big_turn()

    def splay(self):
        if self.is_root():
            return self
        elif self.parent.is_root():
            return self.zig()
        elif self.is_left() == self.parent.is_left():
            return self.zigzig()
        else:
            return self.zigzag()


class TwoThreeTree(Node):
    def usual_paste(self, k, v=None):
        next_branch = self.get_branch(k)
        if next_branch is None:
            self.set_nth_child(new_node, num=self.get_branch_num(k))  # noqa Type checker
            return new_node
        else:
            return next_branch.usual_paste(k, v)

    def paste(self, k, v=None):
        pasted_node = self.usual_paste(k, v)


asd = RedBlackBinaryNode(key=0)
asd.paste(1)
asd.paste(2)
asd.paste(3)
asd.paste(4)
