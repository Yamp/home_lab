from operator import attrgetter
from typing import List

from coding_challenges.algo.geometry.points import Point


class DivideAndConquerSolver:
    def __init__(self, points: List[Point]):
        self.points = sorted(points, key=attrgetter('x'))

    def merge(self, first: int, last: int) -> None:
        ...
