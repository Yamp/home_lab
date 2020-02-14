import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x = pyo.Var(within=pyo.PositiveReals)
model.y = pyo.Var(within=pyo.PositiveReals)

model.sillybound = pyo.Constraint(expr = model.x + model.y <= 2)

model.obj = pyo.Objective(expr = 20 * model.x)

opt = SolverFactory('glpk')
opt.solve_tsp(model)

model.pprint()

print ("------------- extend obj --------------")
model.obj.expr += 10 * model.y


# добавляем или удалям ограничения
model.con = pyo.Constraint(expr=model.v**2 + model.v >= 3)
model.con.deactivate()
model.con.activate()

opt = SolverFactory('glpk')
opt.solve_tsp(model)
model.pprint()
