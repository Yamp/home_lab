from optimization.routes.lkh_adapter import solve_lkh
from optimization.routes.or_tools_adapters import solve_mtsp_ortools
from optimization.routes.tsp_solvers import solve_tsp


def solve_mtsp_lkh(matrix, m, depot=0):
    return solve_lkh(matrix, mtsp=True, vehicles=m)[0]


def solve_mtsp_best(matrix, m, depot=0):
    tours = solve_lkh(matrix, mtsp=True, vehicles=m)[0]
    res = []

    for t in tours:
        sub_matr = matrix[t][:, t]
        indices = solve_tsp(sub_matr, solver='concorde')
        res += [t[indices]]

    return res


def solve_mtsp(matrix, solver, m, depot=0):
    if solver == 'ortools':
        return solve_mtsp_ortools(matrix, m, depot)
    elif solver == 'lkh':
        return solve_mtsp_lkh(matrix, m, depot)
    elif solver == 'best':
        return solve_mtsp_best(matrix, m, depot)
