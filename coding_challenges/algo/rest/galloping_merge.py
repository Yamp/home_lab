
def bin_search(arr, val, first, last):
    """
    Supposing arr is sorted form smaller to bigger values
    """
    while first != last:
        middle = (first + last) // 2
        if arr[middle] < val:
            first = middle
        elif arr[middle] > val:
            last = middle
        else:
            return middle

    return False

def merge(N, M):
    """
    Supposing N >> M
    """
