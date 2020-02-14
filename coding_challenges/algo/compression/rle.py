from itertools import groupby

from typing import Iterable


def str_to_ints(s: Iterable):
    for c in s:
        yield ord(c)


def delta_filter(s: Iterable):
    s = iter(s)
    prev_c = next(s)
    yield prev_c  # yielding first symbol

    for c in s:
        yield c - prev_c
        prev_c = c


def run_length_encode(data: str):
    return ((x, sum(1 for _ in y)) for x, y in groupby(data))


def rle_str(s: Iterable):
    prev_c = next(s := iter(s))

    counter = 1
    for c in s:
        if c == prev_c:
            counter += 1
        else:
            yield counter, prev_c
            counter = 1

        prev_c = c

    yield counter, prev_c


if __name__ == "__main__":
    s = 'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
    print(list(run_length_encode(s)))
    print(list(delta_filter(str_to_ints(s))))
