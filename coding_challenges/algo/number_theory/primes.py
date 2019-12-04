import math
import time
from math import gcd
from random import random
from typing import Tuple


def eratosfen_sieve(n: int):
    is_prime = [True] * n

    for i in range(2, int(n ** 0.5) + 1, 2):
        if is_prime[i]:
            is_prime[i ** 2::i] = [False] * ((n - i) // i - 1)

    return [i for i, a in enumerate(is_prime) if a][2:]


def sanduram_sieve(n: int):
    n = (n - 1) // 2
    is_prime_part = [True] * (n + 1)

    max_i = int(((2 * n + 1) ** 0.5 - 1) / 2)
    for i in range(1, max_i + 1):
        for j in range(1, (n - i) // (2 * i + 1) + 1):
            is_prime_part[2 * i * j + i + j] = False

    return [2] + [2 * i + 1 for i, a in enumerate(is_prime_part) if a and i > 0]


def atkin_sieve(nmax):
    """
    Returns a list of prime numbers below the number "nmax"
    """
    is_prime = dict([(i, False) for i in range(5, nmax + 1)])
    for x in range(1, int(math.sqrt(nmax)) + 1):
        for y in range(1, int(math.sqrt(nmax)) + 1):
            n = 4 * x ** 2 + y ** 2
            if (n <= nmax) and ((n % 12 == 1) or (n % 12 == 5)):
                is_prime[n] = not is_prime[n]
            n = 3 * x ** 2 + y ** 2
            if (n <= nmax) and (n % 12 == 7):
                is_prime[n] = not is_prime[n]
            n = 3 * x ** 2 - y ** 2
            if (x > y) and (n <= nmax) and (n % 12 == 11):
                is_prime[n] = not is_prime[n]
    for n in range(5, int(math.sqrt(nmax)) + 1):
        if is_prime[n]:
            ik = 1
            while ik * n ** 2 <= nmax:
                is_prime[ik * n ** 2] = False
                ik += 1
    primes = []
    for i in range(nmax + 1):
        if i in [0, 1, 4]:
            pass
        elif i in [2, 3] or is_prime[i]:
            primes.append(i)
        else:
            pass
    return primes


def naive_prime_test(a: int) -> bool:
    for i in range(2, int(a ** 0.5) + 1):
        if a % i == 0:
            return False
    return True


def ferma_prime_test(num: int, rounds=100) -> bool:
    if num == 2:
        return True

    for i in range(rounds):
        rnd = random.randrange(2, num)
        if gcd(rnd, num) != 1 or pow(rnd, num, num - 1) != 1:
            return False

    return True


def extract_power_of_two(num: int) -> Tuple[int, int]:
    s = 0
    while (a := divmod(num, 2))[1] == 0:
        s += 1
        num = a[0]

    return s, num


def rabin_miller_prime_test(num: int, rounds=100) -> bool:
    rounds = max(rounds, int(math.log2(num)) * 2)
    ...


if __name__ == "__main__":
    # print(eratosfen_sieve(10000))
    # print(sanduram_sieve(10000))

    start = time.time()
    eratosfen_sieve(10_000_000)
    print(time.time() - start)

    start = time.time()
    atkin_sieve(10_000_000)
    print(time.time() - start)

    # start = time.time()
    # sanduram_sieve(100_000_000)
    # print(time.time() - start)
