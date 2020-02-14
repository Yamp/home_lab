dynamic_table = [0]


def lcs(s1: str, s2: str) -> int:
    l1, l2 = len(s1), len(s2)
    table = [[0] * l2 for _ in range(l1)]

    for i in range(l1 - 1):
        for j in range(l2 - 1):

            table[i + 1][j + 1] = 1 + table[i][j]

            table[i + 1][j] = ...
            table[i][j + 1] = ...

    return table[l1 - 1][l2 - 1]


# largest_increasing_subsequence
def lis(arr):
    table = []
    # lis([], a)
