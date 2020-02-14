import pyomo as pyo


model = None

# concrete model
opt = pyo.SolverFactory('glpk')
opt.solve_tsp(model)

#
