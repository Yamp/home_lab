from typing import Any

import numpy as np


def closest_2deg(n: int):
    i = 1
    while 2 ** i < n:
        i *= 2
    return i


def recursive_fft(x):
    # TODO: think about it, cooley-tukey
    n = len(x)
    if n <= 1: return x

    even = recursive_fft(x[0::2])
    odd = recursive_fft(x[1::2])

    T = [np.exp(-2j * np.pi * k / n) * odd[k] for k in range(n // 2)]
    res = [even[k] + T[k] for k in range(n // 2)] + [even[k] - T[k] for k in range(n // 2)]

    return res


class Polynom:
    def __init__(self, deg: int = 2):
        self.coeffs = np.zeros(deg)

    def __getitem__(self, i: int) -> int:
        if i < len(self.coeffs):
            return self.coeffs[i]
        return 0

    def __setitem__(self, i: int, value: int) -> None:
        self.coeffs[i] = value

    def __call__(self, x) -> Any:
        return self.calc(x)

    @property
    def deg(self) -> int:
        return len(self.coeffs)

    def sum(self, other: 'Polynom') -> 'Polynom':
        """
         TODO: can write normal sum as in
         https://stackoverflow.com/questions/7891697/numpy-adding-two-vectors-with-different-sizes
        """
        res = Polynom(max(self.deg, other.deg))

        for i in range(res.deg):
            res[i] = self[i] + other[i]

        return res

    def calc(self, x) -> Any:
        res = 0
        for c in reversed(self.coeffs):
            res *= x
            res += c
        return res

    def fft(self):
        n = closest_2deg(len(self.coeffs))
        data = np.zeros(n)
        data[:n] = self.coeffs

        T = [np.exp(-2j * np.pi * k / n) * odd[k] for k in range(n // 2)]

        N = len(x)

    def newton_interpolation(self, values):
        ...
        # TODO

    def lagrange_interpolation(self, values):
        ...
        # TODO

    def naive_mult(self, other):
        res = Polynom(self.deg + other.deg)
        for i in range(self.deg):
            for j in range(self.deg):
                ...  # TODO:

    def karatsuba_mult(self, other):
        ...
        # TODO
