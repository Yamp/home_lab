
def extract_digit(num, d):
    return num // 10**(d-1) % 10

def radix_sort(arr, first: int, last: int, digits):

