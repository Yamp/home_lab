from dataclasses import dataclass

from typing import List, Tuple


@dataclass
class Interval:
    start: int
    finish: int
    weight: int


@dataclass
class WeightedIntervalSolver:
    intervals: List[Interval]


def best_weight(intervals: List[Interval], start: int, finish: int) -> Tuple[int, List[int]]:
    weight = best_weight()
    # TODO: finish
