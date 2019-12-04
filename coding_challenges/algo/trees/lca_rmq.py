from dataclasses import dataclass
from typing import Iterable


def get_counter():
    i = 0
    while True:
        yield i
        i += 1


@dataclass
class NlognRMQ:
    data: Iterable

    def preprocess(self):
        ...


class LCATree:
    def __init__(self):
        self.children = []
        self.parent = None
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
