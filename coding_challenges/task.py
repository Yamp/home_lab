from itertools import combinations, chain
from sys import stdin
import math
from collections import defaultdict, deque, Counter


def read_data():
    def read_int(string=None):
        return int(string or input())

    def read_text():
        return stdin.read(-1)

    def read_int_line(string=None):
        return tuple(int(x) for x in (string or input()).split())

    return dict(
        n=read_int(),
        weights=read_int_line()
    )


# -------------------------------------  END OF PERSISTENT -----------------------------------

def powerset(iterable):
    return chain.from_iterable(combinations(iterable, r) for r in range(len(iterable) + 1))


current_best = math.inf


def best_sum(weights, total_sum):
    for i, w in weights:
        weights += []


if __name__ == "__main__":
    input_data = read_data()
    sorted_weights = sorted(input_data['weights'])
    sum_weight = sum(sorted_weights)

    # можно резать ветки, направлять поиск и экономить на повторном рассчете сумм, если все это сохранить
    # и сделать через стек

    all_combs = powerset(tuple(w * 2 for w in input_data['weights']))
    all_sums = tuple(sum(s) for s in all_combs)
    res = min(abs(sum_weight - s) for s in all_sums)
    print(res)
