from dataclasses import dataclass

from typing import List


@dataclass
class Dimensions:
    first: int
    second: int

    def operations(self, other: 'Dimensions'):
        assert self.first == other.second
        return self.first * self.second * other.second


def multiplication_order(matrices: List[Dimensions]):
    ... # TODO: matrix mult order
