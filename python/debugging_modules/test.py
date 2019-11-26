import snoop
from birdseye import eye

snoop.install()


@spy
def factorial(n):
    if n == 0:
        return 1
    else:
        return factorial(n - 1) * n


res = pp(factorial(10))
pp(res)
