from timeit import timeit

import redis

data = range(1_000_000)

r = redis.Redis(host='localhost', port=6379, db=9)
r.flushdb(asynchronous=True)


def tested_func():
    for i in data:
        r[data[i]] = data[i - 100]
        r.get(data[i - len(data) // 2])

print(timeit(tested_func, number=1))
