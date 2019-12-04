import random
import sys
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


# Largest prefix of s[i:] which is also prefix of s
def z_function(s: str) -> np.ndarray:
    """
    Largest prefix of s[i:] which is also prefix of s
    """
    l = len(s)
    res = np.zeros(l, dtype=np.int32)

    first_best, last_best = 0, 0
    for i in range(1, l):
        if last_best > 0:  # if best block ends after i
            res[i] = min(res[i - first_best], last_best - i)  # subblock can be inside or outside

        while i + res[i] < l and s[res[i]] == s[i + res[i]]:
            res[i] += 1

        if i + res[i] > last_best:  # updating best block info
            first_best, last_best = i, i + res[i]

    return res


def prefix_function(s: str) -> np.ndarray:
    """
    Largest prefix which is also suffix of s[:i]
    """
    l = len(s)
    res = np.zeros(l, dtype=np.int32)

    for i in range(1, l):
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
    """
    Last index of each str symbol
    """
    res = {}
    for i, a in enumerate(s):
        res[a] = len(s) - i

    return res


def boyer_moor_horspool_search(needle: str, haystack: str) -> int:
    l_n, l_h = len(needle), len(haystack)
    last_n = l_n - 1
    shifts = stop_symbols(needle[:-1])

    first = 0
    while (last := first + last_n) < l_h:
        if needle == haystack[first:last + 1]:
            return first
        first += shifts.get(haystack[last], l_n)  # shifting

    return -1


def python_native_search(needle: str, haystack: str) -> int:
    return haystack.find(needle)


def rabin_karp_search(
        needle: str, haystack: str,
        hash_mod=sys.maxsize, hash_base=37,
) -> int:
    def str_hash(s: str, start=0):
        for c in s:
            start = (start * hash_base + ord(c)) % hash_mod
        return start

    l_n, l_h = len(needle), len(haystack)
    needle_hash, substr_hash = map(str_hash, [needle, haystack[:l_n]])
    highest_power = pow(hash_base, l_n - 1, hash_mod)  # highest power of hash

    for i in range(l_n, l_h):
        if substr_hash == needle_hash and needle == haystack[i - l_n:i]:
            return i - l_n

        substr_hash -= highest_power * ord(haystack[i - l_n])
        substr_hash = str_hash(haystack[i], substr_hash)

    return -1


def suffix_table(s: str) -> np.ndarray:
    """
    Where to move if strings doesn't match
    """
    l = len(s)
    z = np.zeros(len(s) + 1)

    max_z_idx, max_z = 0, 0
    for i in range(1, l):
        if i <= max_z:
            z[i] = min(max_z - i + 1, z[i - max_z_idx])

        while (i + z[i]) < l and s[l - 1 - z[i]] == s[l - 1 - (i + z[1])]:
            z[i] += 1

        if i + z[i] - 1 > max_z:
            max_z_idx = i
            max_z = i + z[i] - 1

    res = np.zeros(len(s) + 1)
    for i in reversed(range(0, l)):
        res[l - z[i]]

    # for i in reversed(range(l)):
    #     if s[i] == s[res[i]]:

    return res


def boyer_moor_search(needle: str, haystack: str) -> int:
    ...
    # TODO:


# --------------------------------------------- Tests ----------------------------------------

def test_substring_search(search_func):
    data = (['1'] * 10000 + ['0'] * 10000)
    random.shuffle(data)
    str_ = ''.join(data)

    haystack = str_

    results = []
    for i in range(1, 50):
        needle = haystack[-i:] + '11'  # salt to sometimes get -1
        results += [haystack.find(needle)]
        assert search_func(needle, haystack) == haystack.find(needle), f"{needle}, {haystack}"

    print(search_func.__name__, 'works fine!')
    # print(results)


if __name__ == "__main__":
    test_substring_search(python_native_search)
    test_substring_search(naive_str_search)
    test_substring_search(kmp_search)
    test_substring_search(boyer_moor_horspool_search)
    test_substring_search(rabin_karp_search)
