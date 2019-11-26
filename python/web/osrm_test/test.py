import random
from time import time

import osrm

center = (37.6373, 55.7253)


def random_point():
    std = 0.5
    a, b = random.random() * std, random.random() * std
    return center[0] + a, center[1] + b


def make_experiment():
    MyConfig = osrm.RequestConfig("localhost:5000/v1/driving")
    for size in range(2000, 2001, 1):
        points = [random_point() for i in range(size)]
        st = time()
        res = osrm.table(points, points, url_config=MyConfig)
        print(res[0])
        print(size, round(time() - st, 4))

make_experiment()

# 5k 30s
# 10k 109s
