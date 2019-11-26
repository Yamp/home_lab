cpdef int test(int x):
    cdef int y = 0
    i = 0

    for i in range(x):
        y += 1

    return y
