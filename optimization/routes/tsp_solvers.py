from time import time
import numpy as np

from optimization.routes.concorde_adapter import solve_concorde
from optimization.routes.lkh_adapter import solve_lkh


def solve_tsp_lkh(matrix):
    return solve_lkh(matrix)


def solve_tsp_concorde(matrix):
    return solve_concorde(matrix)


def solve_tsp(matrix, solver):
    """ Решаем обычного коммивояжера """
    start = time()

    if solver == 'concorde':
        res = solve_tsp_concorde(matrix)
    else:
        res = solve_tsp_lkh(matrix)

    print(solver, time() - start)
    print(res[1])

    return np.array(res[0][0])
