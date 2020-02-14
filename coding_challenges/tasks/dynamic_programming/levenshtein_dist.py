from functools import lru_cache


@lru_cache(maxsize=1000000)
def cached_dist(str1: str, str2: str) -> int:
    if not str1 or not str2:
        return len(str1) + len(str2)

    if str1[0] == str2[0]:
        return cached_dist(str1[1:], str2[1:])

    return 1 + min(
        cached_dist(str1, str2[1:]),
        cached_dist(str1[1:], str2),
        cached_dist(str1[1:], str2[1:]),
    )


def tabled_dist(str1: str, str2: str) -> int:
    # can fix memory usage
    l1, l2 = len(str1), len(str2)
    table = [[0] * l2 for _ in range(l1)]

    table[0][:] = range(l2)
    for i in range(l1):
        table[i][0] = i

    for i in range(1, l1):
        for j in range(1, l2):
            table[i][j] = 1 + min(
                table[i - 1][j - 1] - (str1[i] == str2[j]),
                table[i][j - 1],
                table[i - 1][j]
            )

    return table[l1 - 1][l2 - 1]


def damerau_levenshtein_distance(str1: str, str2: str) -> int:
    l1, l2 = len(str1), len(str2)
    table = [[0] * (l2 + 1) for _ in range(l1 + 1)]

    table[0][:] = range(-1, l2)
    for i in range(-1, l1):
        table[i][-1] = i

    for i in range(l1):
        for j in range(l2):
            if str1[i] == str2[j]:
                table[i][j] = table[i - 1][j - 1]
                continue

            table[i][j] = 1 + min(
                table[i - 1][j - 1],
                table[i][j - 1],
                table[i - 1][j],
            )

            if i * j != 0 and str1[i - 2:i] == reversed(str2[j - 2:j]):
                table[i][j] = min(table[i][j], table[i - 2][j - 2])

    return table[l1 - 1][l2 - 1]


a = 'CONEHEAD'
b = 'CONNECT'
dist = cached_dist(a, b)
print(dist)
dist = tabled_dist(a, b)
print(dist)
