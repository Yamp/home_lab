from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from operator import itemgetter

from fn.iters import group_by
from py3votecore.schulze_method import SchulzeMethod

from py3votecore.condorcet import CondorcetHelper
from typing import List, Tuple

from sortedcontainers import SortedList

ballots = [
    {"count": 3, "ballot": [["A"], ["C"], ["D"], ["B"]]},
    {"count": 9, "ballot": [["B"], ["A"], ["C"], ["D"]]},
    {"count": 8, "ballot": [["C"], ["D"], ["A"], ["B"]]},
    {"count": 5, "ballot": [["D"], ["A"], ["B"], ["C"]]},
    {"count": 5, "ballot": [["D"], ["B"], ["C"], ["A"]]}
]
res = SchulzeMethod(ballots, ballot_notation=CondorcetHelper.BALLOT_NOTATION_GROUPING).as_dict()
print(res)


@dataclass
class Ballot:
    """
    Допускаются отдинаковые ранги для разных кандидатов
    """
    total_num: int
    ranking: SortedList['Vote']  # Tuples of (rank, candidate id)

    def best(self):
        rank, res = self.ranking[-1], []
        for r, c_id in reversed(self.ranking):
            if r != rank:
                break
            res += [c_id]

        return rank, res

    def pop_best(self):
        rank, res = self.ranking[-1], []
        while self.ranking:
            r, c_id = self.ranking.pop()
            if r != rank:
                break
            res += [c_id]

        return rank, res


@dataclass
class Vote:
    ballot: Ballot
    rank: int
    proportion: float = 1  # TODO: replace with fraction?


def borda_count(ballots: List[Ballot]):
    res = defaultdict(int)

    for b in ballots:
        for c_id, rank in b.ranking:
            res[c_id] += b.total_num - rank  # can be any function

    return sorted(res.items(), key=itemgetter(1))


def approvement_vote(ballot: List[Ballot], ):
    ...

def schulze_method(ballot: List[Ballot]):
    ...  # TODO:


def stv(ballots: List[Ballot], results_num: int):
    ballots = deepcopy(ballots)
    votes = defaultdict(list)

    for b in ballots:
        r, c_ids = b.pop_best()

