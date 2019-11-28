from typing import Tuple


def euclid_gcd(a: int, b: int) -> int:
    while a != 0 and b != 0:
        a, b = b % a, a
    return a + b


def extended_gcd_recursive(a: int, b: int) -> Tuple[int, int, int]:
    """
    Returns tuple (gcd, x, y) such that x * a + y * b = gcd
    gcd = x_p * (b mod a) + y_p * a = x_p * (b - b/a*a) + y_p * a = b * x_p + a * (y_p - b/a * x_p)

    x = (y_p - b/a * x_p);
    y = x_p
    """
    if a == 0:
        return b, 0, 1

    gcd, x_prev, y_prev = extended_gcd_recursive(b % a, a)
    return gcd, y_prev - b // a * x_prev, x_prev


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    while a != 0 and b != 0:
        d, r = divmod(b, a)
