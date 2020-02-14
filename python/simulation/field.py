from collections import deque, defaultdict
from enum import Enum
from itertools import product
import random


class Color(Enum):
    GREEN = 0
    YELLOW = 1
    ORANGE = 2
    BLUE = 3
    CYAN = 4
    PINK = 5
    VIOLET = 6

    MAX_COLOR = 6


class Field:
    """
    Размер поля 9*9
    """

    __slots__ = ('data', 'free')

    def __init__(self):
        self.data = {}
        self.free = set()

    def is_full(self):
        return len(self.free) == 0

    def add_random_ball(self):
        color = random.randint(0, Color.MAX_COLOR)
        cell = random.choice(self.free)

        self.data[cell] = color
        self.free.remove(cell)

    def estimate_position(self):
        return len(self.free)

    def is_empty(self, cell):
        return cell in self.free

    def is_valid(self, cell):
        return 0 <= cell[0] <= 8 and 0 <= cell[1] <= 8

    def neighbours(self, cell):
        candidates = (
            (cell[0] + 1, cell[1]),
            (cell[0] - 1, cell[1]),
            (cell[0], cell[1] + 1),
            (cell[0], cell[1] - 1),
        )

        return (c for c in candidates if self.is_valid(c))

    def can_move(self, c1, c2):
        # TODO: можно поддерживать связность
        visited = defaultdict(bool)
        queue = deque()
        queue.append(c1)
        visited[c1] = True

        while queue:
            if (curr_cell := queue.popleft()) == c2:
                return True

            visited[curr_cell] = True
            if self.is_empty(curr_cell) and not visited[curr_cell]:
                queue.append(self.neighbours(curr_cell))

        return False

    def just_move(self, c1, c2):
        self.free.add(c1)
        self.free.remove(c2)
        self.data[c1] = self.data[c2]


class Simulator:
    def simulate(self, field, max_depth):
        ...
