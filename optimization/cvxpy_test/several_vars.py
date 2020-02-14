import cvxpy as cp

x, y = cp.Variable(), cp.Variable()  # Создаем скалярные переменные

rho = cp.Parameter(nonneg=True, value=2)  # Задаем параметр

prob = cp.Problem(  # создаем проблему
    objective=cp.Minimize((x - y) ** 2),
    constraints=[x + y == 1, x - y >= 1],
)
res = prob.solve_tsp()
print(f'{prob.status=}, {prob.value=}, {x.value=}, {y.value=} {res=}')


