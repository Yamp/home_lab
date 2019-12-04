from typing import Callable


def newton_root(
        f: Callable, df: Callable,
        point: float, x_tol=1e-5
) -> float:
    """ f is the f(x) and df is the f'(x) """
    while True:
        new_point = point - f(point) / df(point)

        if abs(point - new_point) < x_tol:
            return new_point

        point = new_point
