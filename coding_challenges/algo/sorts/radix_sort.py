def extract_digit(num, d):
    return num // 10 ** (d - 1) % 10


def counting_sort(data, items_num=10, key=lambda x: x):
    counts = [0] * items_num
    res = [None] * data

    for d in data:
        counts[key(d)] += 1





def radix_sort(arr, first: int, last: int, digits):
    ...
