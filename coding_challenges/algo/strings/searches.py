import random
from typing import List

import numpy as np


# largest common prefix
def dynamic_lcp(str1: str, str2: str) -> List[List[int]]:
    n1, n2 = len(str1), len(str2)
    lcp_table = [[0] * (n2 + 1) for _ in range(n1 + 1)]  # (n1 + 1) * (n2 + 1)

    for i in reversed(range(n1)):
        for j in reversed(range(n2)):
            lcp_table[i][j] = lcp_table[i + 1][j + 1] + (str1[i] == str2[j])

    return lcp_table


def polynom_hash(str1: str) -> List[int]:
    results = []

    res = 0
    for a in str1:
        res *= 37
        res += ord(a)
        res %= 2 ** 32 - 1

        results += res

    return results


def naive_str_search(needle: str, haystack: str) -> int:
    l_n, l_h = len(needle), len(haystack)

    for i in range(l_h - l_n + 1):
        if haystack[i:i + l_n] == needle:
            return i

    return -1


def prefix_function(s: str) -> np.ndarray:
    l = len(s)
    res = np.zeros(l, dtype=np.int32)

    for i in range(1, len(s)):
        current_border = res[i - 1]
        while current_border > 0 and s[current_border] != s[i]:
            current_border = res[current_border - 1]

        if s[current_border] == s[i]:
            res[i] = current_border + 1

    return res


def kmp_search(needle: str, haystack: str) -> int:
    l_n, l_h = len(needle), len(haystack)
    pref = prefix_function(needle)

    current_border = 0
    for i in range(l_h):
        while current_border > 0 and needle[current_border] != haystack[i]:
            current_border = pref[current_border - 1]

        if needle[current_border] == haystack[i]:
            current_border += 1

        if current_border == l_n:
            return i - l_n + 1

    return -1


def stop_symbols(s: str):
    res = {}
    for i, a in enumerate(s[:-1]):
        res[a] = i

    return res


def boyer_moor_search(needle: str, haystack: str) -> int:
    ...
    # TODO:


def rabin_karp(needle: str, haystack: str) -> int:
    ...
    # TODO:


def lcp_hash(str1: str, str2: str) -> int:
    hash1 = polynom_hash(str1)
    hash2 = polynom_hash(str2)

    ...
    # TODO:


def test_substring_search(search_func):
    data = (['1'] * 10000 + ['0'] * 10000)
    random.shuffle(data)
    str_ = ''.join(data)

    haystack = str_

    results = []
    for i in range(1, 50):
        needle = haystack[-i:] + '11'  # salt to sometimes get -1
        results += [haystack.find(needle)]
        assert search_func(needle, haystack) == haystack.find(needle)

    print(search_func.__name__, 'works fine!')
    # print(results)


if __name__ == "__main__":
    test_substring_search(naive_str_search)
    test_substring_search(kmp_search)
