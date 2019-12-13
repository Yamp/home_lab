import numpy as np


def weights_one_machine(durations, deadlines, prices):
    n = len(durations)
    total = sum(durations)
    f = np.full((n, n), np.inf)  # TODO: bullshit
    f[0, :] = 0

    for j in range(n):
        for t in range(deadlines[j]):
            if f[j - 1][t] + prices[j] < f[j - 1][t - durations[j]]:
                f[j][t] = f[j - 1][t] + prices[j]
            else:
                f[j][t] = f[j - 1][t - prices[j]]

        for t in range(deadlines[j], total):
            f[j][t] = f[j][deadlines[j]]
