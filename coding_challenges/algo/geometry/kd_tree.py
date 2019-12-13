from operator import attrgetter
from typing import List

from coding_challenges.algo.geometry.points import Point


class KDTree:
    def __init__(self, points: List[Point]):
        ...

    def build_tree(self, points):
        x_sorted = sorted(points, key=attrgetter('x'))
        y_sorted = sorted(points, key=attrgetter('y'))


