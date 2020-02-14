import cvxpy as cp
import numpy
import matplotlib.pyplot as plt

from multiprocessing import Pool

# Problem data.
n, m = 15, 10
A, b = numpy.random.randn(n, m), numpy.random.randn(n)
gamma = cp.Parameter(nonneg=True)  # параметры LASSO

# Construct the problem.
x = cp.Variable(m)
error = cp.sum_squares(A * x - b)
prob = cp.Problem(
    objective=cp.Minimize(error + gamma * cp.norm(x, 1))
)

# Construct a trade-off curve of ||Ax-b||^2 vs. ||x||_1
sq_penalty, l1_penalty, x_values = [], [], []
gamma_vals = numpy.logspace(-4, 6)

# решаем задачу для кучи разных gamma
for val in gamma_vals:
    gamma.value = val
    prob.solve_tsp()

    sq_penalty += [error.value]
    l1_penalty += [cp.norm(x, 1).value]
    x_values += [x.value]

plt.rc("text", usetex=True)
plt.rc("font", family="serif")
plt.figure(figsize=(6, 10))

# Plot trade-off curve.
plt.subplot(211)
plt.plot(l1_penalty, sq_penalty)
plt.xlabel(r'$\|x\|_1$', fontsize=16)
plt.ylabel(r'$\|Ax-b\|^2$', fontsize=16)
plt.title('Trade-Off Curve for LASSO', fontsize=16)

# Plot entries of x vs. gamma.
plt.subplot(212)
for i in range(m):
    plt.plot(gamma_vals, [xi[i] for xi in x_values])
plt.xlabel(r'$\gamma$', fontsize=16)
plt.ylabel(r'$x_i$', fontsize=16)
plt.xscale("log")
plt.title(r'Entries of x vs. $\gamma$', fontsize=16)

plt.tight_layout()
plt.show()
