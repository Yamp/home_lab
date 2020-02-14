from _bisect import bisect_left
from bisect import insort, bisect
from collections import deque
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple, Type, Any

import numpy as np


# TODO: 2-3-trees, 2-3-4-tree, B+, B*, R-tree, kd-tree
# TODO: finger tree
# TODO: add building perfect tree from an array
@dataclass
class Node:
    """
    Rules:
    1) keys are gonna be sorted in ascending order
    2) < -> left >= -> right
    3) The root is a fake top node

    TODO: successor, predessor
    """
    parent: Optional['Node'] = None
    children: List = field(default_factory=list)

    keys: List = field(default_factory=list)
    values: List = field(default_factory=list)

    # ----------------------------------- access methods ------------------------------------------

    def __str__(self):
        return f'Node({self.keys})'

    def real_children(self) -> Iterable['Node']:
        return (c for c in self.children if c is not None)

    # nth-parent or root
    def nth_parent(self, n: int) -> 'Node':
        """
        nth parent or root
        """
        return self if n <= 0 else self.parent.nth_parent(n - 1)

    def grandpa(self) -> 'Node':
        return self.nth_parent(2)

    # num of child to search k in
    def get_branch_num(self, k) -> int:
        """
        Number of child for search
        """
        for i, key in enumerate(self.keys):
            if k < key:
                return i
        else:
            return len(self.children) - 1

    # check if i'm n'th child
    def is_nth_child(self, n: int) -> bool:
        return (
                n in self.parent.children[n]
                and self is self.parent.children[n]
        )

    def is_leaf(self) -> bool:
        return not any(self.children)

    def is_root(self) -> bool:
        return self.parent is None \
               or self.parent is self

    def set_nth_child(self, child: 'Node', num: int) -> None:
        if child is not None:
            child.parent = self
        self.children[num] = child

    def _index(self, k) -> int:
        try:
            return self.children.index(k)
        except ValueError:
            return -1

    def get_my_child_num(self):
        for i, c in enumerate(self.parent.children):
            if self is c:
                return i

    def add_new_value(self, k, v=None):
        new_node = self.__class__(keys=[k], values=[v], parent=self)
        self.children += [None]

        self.set_nth_child(new_node, num=len(children) - 1)  # noqa Type checker

    # ---------------------------- Iterators -----------------------------------------------

    def nodes_dfs(self):
        """
        Time of going into node during dfs
        """
        stack = deque()
        stack += [self]

        while stack:
            node = stack.pop()
            yield node
            for c in reversed(node.real_children()):  # to process children left to right
                stack += [c]

    def nodes_topological(self):
        """
        Topological order.
        Time of dfs going out
        """
        stack = deque()
        stack += [(self, 'in')]

        while stack:
            node, event = stack.pop()

            if event == 'out':
                yield node
            else:
                for c in node.real_children():
                    stack += [(c, 'in')]
                stack += [(node, 'out')]

    def nodes_dfs_inout(self):
        stack = deque()
        stack += [(self, 'in')]

        while stack:
            node, event = stack.pop()
            yield node, event

            if event == 'in':
                for c in node.real_children():
                    stack += [(c, 'in')]
                stack += [(node, 'out')]

    # yield node and (key, value) index
    def nodes_sorted(self):
        """
        Dfs middle time
        """
        stack = deque()
        stack += [(self, -1, 'in')]

        while stack:
            node, i, event = stack.pop()

            if event == 'middle':
                yield node, i
            if event == 'in':
                alive_children = list(node.real_children())[::-1]

                if len(alive_children) < 2:
                    # Case for None children. Mainly for binary trees
                    stack += [(node.children[1], -1, 'in')] if node.children[1] is not None else []
                    stack += [(node, 0, 'middle')]
                    stack += [(node.children[0], -1, 'in')] if node.children[0] is not None else []
                else:
                    res = [None] * (2 * len(alive_children) - 1)
                    res[::2] = [(c, -1, 'in') for c in alive_children]
                    res[1::2] = [  # interleaving children with proper key of node
                        (node, i, 'middle')
                        for i in range(len(alive_children) - 1)
                    ]
                    stack += res

    def nodes_bfs(self):
        """
        Bfs in time
        """
        queue = deque()
        queue += [self]

        while queue:
            node = queue.popleft()
            yield node
            for c in node.real_children():
                queue += [c]

    def nodes_bfs_out(self):
        """
        Bfs in time
        """
        queue = deque()
        queue += [(self, 'in')]

        while queue:
            node, event = queue.popleft()

            if event == 'out':
                yield node
            else:
                for c in node.real_children():
                    queue += [(c, 'in')]
                queue += [(node, 'out')]

    # yield node and (key, value) index
    def nodes_bfs_middle(self):
        """
        Bfs middle time
        """
        stack = deque()
        stack += [(self, -1, 'in')]

        while stack:
            node, i, event = stack.popleft()

            if event == 'middle':
                yield node, i
            if event == 'in':
                alive_children = list(node.real_children())

                if not alive_children:
                    stack += [(node, 0, 'middle')]
                else:
                    res = 2 * len(alive_children) - 1
                    res[::2] = alive_children
                    res[1::2] = [  # interleaving children with proper key of node
                        (node, i, 'middle')
                        for i in range(len(alive_children) - 1)
                    ]
                    stack += res

    # ---------------------------- Search operations ---------------------------------------

    # branch for father search
    def get_branch(self, k) -> 'Node':
        """
        Appropriate branch for search
        """
        for i, key in enumerate(self.keys):
            if k < key:
                return self.children[i]
        else:
            return self.children[-1]

    def usual_paste(self, k, v=None):
        next_branch = self.get_branch(k)
        if next_branch is None:
            # new_node = self.__class__(keys=[k], values=[v], parent=self)
            new_node = self.__class__()
            new_node.keys = [k]
            new_node.values = [v]
            self.set_nth_child(new_node, num=self.get_branch_num(k))  # noqa Type checker
            return new_node
        else:
            return next_branch.usual_paste(k, v)

    def find(self, k) -> Any:
        if i := self._index(k) != -1:
            return self.values[i]
        elif self.is_leaf():
            return None
        return self.get_branch(k).find(k)

    def found(self, k):
        return k in self.keys

    def paste(self, k, v=None):
        return self.usual_paste(k, v)

    # def successor(self):
    #

    def get_sorted_array(self):
        res = [n.keys[i] for n, i in self.nodes_sorted()]
        return res

    # ---------------------------- Methods for tree manipulation ---------------------------

    def replace_by(self, subtree: Optional['Node']):
        """ Replace this subtree with given """
        num = self.get_my_child_num()
        self.parent.set_nth_child(subtree, num)
        return self

    def remove_subtree(self):
        return self.replace_by(None)

    def swap_with(self, other: 'Node') -> 'Node':
        self.replace_by(other)
        other.replace_by(self)
        return self

    def add_child(self, key, value=None):
        ...  # TODO
        # insort(self.keys)
        # self.children


@dataclass
class BinaryNode(Node):
    children: List[Optional['BinaryNode']] = field(default_factory=list)
    parent: Optional['BinaryNode'] = None
    keys: List = field(default_factory=list)
    values: List = field(default_factory=list)

    def __init__(self):
        super().__init__()

        self.children = [None, None]
        self.parent = None

        self.keys = [None]
        self.values = [None]

    def __str__(self):
        return f'Node({self.key})'

    def __repr__(self):
        return str(self)

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
        if value is not None:
            value.parent = self

    @property
    def right(self) -> Optional['BinaryNode']:
        return self.children[1]

    @right.setter
    def right(self, value):
        self.children[1] = value
        if value is not None:
            value.parent = self

    def initialize(self, **kwargs):
        fields = {'key', 'value'}

        for f, val in kwargs.items():
            if f in fields:
                setattr(self, f, val)

        self.set_left(kwargs.get('left', None))
        self.set_right(kwargs.get('right', None))

        return self

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

    def set_child(self, child: Optional['BinaryNode'], is_left: bool):
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

    def find_node(self, key) -> Optional['BinaryNode']:
        if self.key == key:
            return self
        elif branch := self.get_branch(key) is None:
            return None
        return branch.find(key)

    # ---------------------------- Methods for tree manipulation ---------------------------

    def replace_by(self, subtree: Optional['BinaryNode']):
        """
        Speedup of the common case
        Replace this subtree with given
        """
        self.parent.set_child(subtree, self.is_left())

    def split_by(self, key) -> Tuple[Optional['BinaryNode'], Optional['BinaryNode']]:
        try:
            left, right = self.get_branch(key).split_by(key)
        except AttributeError:
            # should return self and None if there's no child
            left = right = None

        if key > self.key:
            self.right = left
            return self, right
        else:
            self.left = right
            return left, self

    # ---------------------------- Methods for balancing -----------------------------------

    def small_turn(self) -> 'BinaryNode':
        """
        The only possible small turn for self
        The picture is for self.is_left = True, so rotating to right
        (to_left = False)
                P           self
               / \          / \
            self ...  =>  ...  P
             / \              / \
           ...  C            C  ...

        Returns self
        """
        to_left = not self.is_left()  # if i'm left, I can rotate only to right
        p = self.parent
        c = self.get_child(is_left=to_left)

        self.set_child(p, is_left=to_left)
        p.set_child(c, is_left=not to_left)
        p.replace_by(self)

        return self

    def promote(self) -> 'BinaryNode':
        """ Just alias """
        return self.small_turn()

    def big_turn(self) -> 'BinaryNode':
        """
        The only possible big turn for self
        The picture is for self.is_left = True, so rotating to right
        (to_left = False)
                G              self
               / \             /  \
             ...  P     =>    A    B
                 / \         / \  / \
              self ...     ... M N  ...
              / \
             M  N
        Returns self
        """
        return self.small_turn().small_turn()

    def rotate(self, to_left):
        if to_left:
            self.right.small_turn()
        else:
            self.left.small_turn()


@dataclass
class RedBlackBinaryNode(BinaryNode):
    parent: Optional['RedBlackBinaryNode'] = None
    _is_black: bool = True

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
                if not self.parent.is_root() and self.is_left() != self.parent.is_left():
                    # 4 case
                    self.small_rotate_to(left=is_left_rotate)
                elif not self.parent.is_root():
                    # 5 case
                    self.rotate_to(left=is_left_rotate)

    def paste(self, k, v=None):
        pasted_node = self.usual_paste(k, v)
        pasted_node.make_red()
        pasted_node.balance()
        return pasted_node


class AATreeNode(BinaryNode):
    """
    Mostly like red-black
    On one level only one son and only right
    """

    def __init__(self):
        super().__init__()

        self.children = [None, None]
        self.parent = None

        self.keys = [None]
        self.values = [None]

        # this is like height, but doesn't include "red" nodes
        self.level: int = 1  # 1 is leaf level

    # ---------------------------------- balancing -------------------------------------

    # delete left "red" node
    def skew(self):
        l = self.left
        level = l.level if l else None

        if self.level == level:
            self.rotate(to_left=False)
            return True

        return False

    # delete 2 right "red" nodes
    def split(self):
        r = self.right
        rr = r.right if r else None
        level = rr.level if rr else None

        if self.level == level:
            r.level += 1
            r.promote()
            return True

        return False

    def decrease_level(self):
        l, r = self.left, self.right
        new_level = min(l.level if l else 0, r.level if r else 0) + 1

        if new_level < self.level:
            self.level = new_level

            if r is not None:
                r.level = new_level

            return True

        return False

    def balance_node(self):
        # TODO: conditions?
        self.decrease_level()
        self.skew()
        self.split()

    def balance(self):
        """ first balanced is parent """
        p = self
        while not p.is_root():
            p = p.parent
            p.balance_node()

    # ----------------------------- operations -------------------------------------

    def paste(self, k, v=None):
        new = self.usual_paste(k, v)
        new.balance()

    def delete(self):
        succ = self.node_successor()
        self.key = succ.key, self.value = succ.value

        succ.remove_subtree()
        succ.parent.balance()


@dataclass
class AVLBinaryNode(BinaryNode):
    height: int = 0

    def get_balance(self):
        if self.left.height - self.right.height:
            pass

    def balance(self, k, v=None):
        self.usual_paste(k, v)

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
            # return new_node
        else:
            return next_branch.usual_paste(k, v)

    def paste(self, k, v=None):
        pasted_node = self.usual_paste(k, v)


class SearchTree():
    def __init__(self, node_class):
        self.fake_node = node_class()

        self.fake_node = self.children[0]


class BTreeNode(Node):
    T = 5

    def is_overfilled(self):
        return len(self.children) > 2 * self.T

    def is_undefilled(self):
        return len(self.children) < self.T

    def find_node(self, key) -> 'BTreeNode':
        res = self
        while not res.is_leaf():
            res = res.get_branch(key)
        return res

    def paste(self, key, value=None):
        node = self.find_node(key)
        # node.
        ...

    def split(self):
        l = len(self.keys)
        assert l >= 2

        middle = len(self.keys) // 2
        r_keys, r_vals = self.keys[:middle], self.values[:middle]
        l_key, l_vals = self.keys[middle + 1:], self.values[middle + 1:]
        m_key, m_val = self.keys[middle], self.values[middle]

        self.parent.add_child(m_key, m_val)  # TODO: add subtrees

    def delete(self, key):
        res = self
        while not res.is_leaf():
            res = res.get_branch(key)
        return res

    def delete_from_leaf(self, key):
        i = bisect_left(self.keys, key)
        val = self.values[i]
        del self.keys[i]
        del self.values[i]
        return val


def tree_sort(node_class: Type['Node'], data: np.ndarray):
    node = node_class()
    node.keys = [data[0]]

    for d in data[1:]:
        node.paste(d)
    return node.get_sorted_array()


def test_tree_sort(node_class):
    data = np.arange(0, 3)
    np.random.shuffle(data)
    data = [0, 1, 2]
    res = tree_sort(node_class, data)
    print(data, res)
    assert res == sorted(data)
    print(node_class.__name__, 'sorting works fine!')


if __name__ == "__main__":
    # test_tree_sort(BinaryNode)  # OK!
    test_tree_sort(AATreeNode)
