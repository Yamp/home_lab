
dynamic_table = [0]

def lcs(a: str, b: str) -> int:
    res = 1

    if a[0] == b[0]:
        res += 1

    l1 = lcs(a[1:], b)
    l2 = lcs(a, b[1:])

    res += max(l1, l2)

    return res


# largest_increasing_subsequence
def lis(arr):
    table = []
    # lis([], a)
