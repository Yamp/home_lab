from sys import stdin, stdout

from attr import dataclass
from typing import Collection, List, Dict

from more_itertools import powerset

# Лидер по кондорсе
# Лидер по очкам
# Single transferable vote

@dataclass
class CoopGame:
    N: int  # players number

    #  result of coalition
    def val(self, coalition: Collection) -> int:
        ...

    def is_core(self, x: List[int]):
        # x is one of solutions
        return sum(x) == self.val(range(self.N))

    def excess(self, x: List[int], coalition: Collection) -> int:
        return self.val(coalition) - sum(x[i] for i in coalition)

    def all_coalitions(self):
        return powerset(range(self.N))

    def excess_vector(self, x: List[int]):
        return sorted(
            (self.excess(x, c) for c in self.all_coalitions()),
            reverse=True
        )

    def prenucleolus(self):
        # all x vectors minimizing excess_vector
        # существует и единственный
        ...


class MariageMatching:
    def __init__(self, men, women):
        self.men: Dict[List] = men
        self.women: Dict[List] = women
        self.N = len(self.men)

    def find_matching(self):
        mans_match, womans_match = [None] * self.N, [None] * self.N

        while not all(mans_match):
            for m, mpref in self.men:
                w = mpref[0]
                prev_match = None
                if womans_match[w] is not None or (prev_match := womans_match[w]) < m:  # TODO: bullshit
                    mans_match[m] = w
                    womans_match[w] = m
                    if prev_match:
                        mans_match[prev_match] = None
                else:
                    mpref.pop_front()

