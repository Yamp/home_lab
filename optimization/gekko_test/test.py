from gekko import GEKKO

# Initialize Model
m = GEKKO(remote=False)

# initialize variables
values = [1, 5, 5, 1]
x1, x2, x3, x4 = xs = [m.Var(value=values[i], lb=1, ub=5) for i in range(4)]

# Equations
eq = m.Param(value=40)
m.Equation(x1 * x2 * x3 * x4 >= 25)
m.Equation(x1 ** 2 + x2 ** 2 + x3 ** 2 + x4 ** 2 == eq)

# Objective
m.Obj(x1 * x4 * (x1 + x2 + x3) + x3)

# Set global options
m.options.IMODE = 3  # steady state optimization
m.options.SOLVER = 3  # by default it's 3 (ipopt)

# Solve simulation
m.solve_tsp()

print('Results')
print([x.value for x in xs])
