

def oom_sort(arr, m):
    """
    Supposing len(arr) >> mem
    """
    buffer = [None] * (2*m)

    for i in range(m):
        buffer[i] = arr.pop()
