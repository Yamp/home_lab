from collections import defaultdict
from dataclasses import dataclass
from itertools import count
from typing import Iterable, List

from coding_challenges.algo.structures.disjoint_set import UnionFind
from coding_challenges.algo.trees.all_trees import Node


@dataclass
class RMQRequest:
    first: int
    last: int


@dataclass
class LCARequest:
    a: int
    b: int


@dataclass
class NlognRMQ:
    data: Iterable

    def preprocess(self):
        ...


class LCATree(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ancestors = []
        self.in_time = None
        self.out_time = None

    def set_times(self, counter):
        self.in_time = next(counter)
        for c in self.children:
            c.set_times(counter)
        self.out_time = next(counter)

    def is_ancestor(self, other: 'LCATree'):
        """ self is a ancestor of other """
        return self.in_time < other.in_time and self.out_time > other.out_time

    def build_ancestors(self):
        ...


class TarjanTreeNode(LCATree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num = next(self.counter)
        self.requests_lists = []


class TarjanTree:
    def __init__(self):
        self.counter = count()
        self.sets = UnionFind(1234)  # TODO: bullshit
        self.node = TarjanTreeNode()
        self.requests = defaultdict(list)

    def create_requests(self, requests: List[LCARequest]):
        for r in requests:
            self.requests[r.a] += r.b
            self.requests[r.b] += r.a

    def tarjan_offline_lca(self, requests: List[LCARequest]):
        visited = defaultdict(bool)

        for n, e in self.node.nodes_dfs_inout():
            if e == 'in':
                visited[n.num] = True

            self.sets.union(n.parent.num, n.num)
            visited[n.num] = True
