import cvxpy as cp
import numpy as np

m, n = 30, 20  # создаем матрицу и вектор (уравнений больше чем переменых)
A, b = np.random.randn(m, n), np.random.randn(m)

# Создаем вектор переменных
x = cp.Variable(n)
constraints = [0 <= x, x <= 1]
prob = cp.Problem(
    objective=cp.Minimize(cp.sum_squares(A*x - b)),
    constraints=constraints,
)

# The optimal objective value is returned by `prob.solve()`.
result = prob.solve_tsp()
# The optimal value for x is stored in `x.value`.
print(x.value)
# The optimal Lagrange multiplier for a constraint is stored in
# `constraint.dual_value`.
print(constraints[0].dual_value)
