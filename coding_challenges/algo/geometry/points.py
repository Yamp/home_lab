from dataclasses import dataclass
import numpy as np


@dataclass
class Point:
    vec: np.array

    @property
    def x(self):
        return self.vec[0]

    @x.fset
    def x(self, val):
        self.vec[0] = val

    @property
    def y(self):
        return self.vec[1]

    @y.fset
    def y(self, val):
        self.vec[1] = val

    def __abs__(self):
        return np.linalg.norm(self.vec)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.vec + other.vec)
