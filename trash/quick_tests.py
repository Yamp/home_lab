import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from statsmodels.nonparametric.kernel_regression import KernelReg


def get_maxes(arr):
    maxes_num = 2
    cur_maxes = []
    x, Y = [], []

    for i, a in enumerate(arr):
        if len(cur_maxes) == 0 or a > cur_maxes[0]:
            if len(cur_maxes) > maxes_num:
                del cur_maxes[0]
            cur_maxes += [a]
            cur_maxes.sort()
            x += [i]
            Y += [a]

    return np.array(x), np.array(Y)


N = 1000
arr = np.random.rand(N) ** 2 * np.arange(N) ** 2 * 0.5

x, Y = get_maxes(arr)

kr = KernelReg(Y,x,'c')
res, y_std = kr.fit(np.arange(N))

plt.plot(arr, color="b")
# plt.plot(x, Y, color="r")
plt.plot(res, color="g")

plt.show()
