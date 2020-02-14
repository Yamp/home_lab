import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()  # модель без параметров
model.nVars = pyo.Param(initialize=4)  # количество переменных
model.N = pyo.RangeSet(model.nVars)  #
model.x = pyo.Var(model.N, within=pyo.Binary)  # создаем бинарные переменные
model.obj = pyo.Objective(expr=pyo.summation(model.x))  # objective — просто их сумма

model.cuts = pyo.ConstraintList()  # пустой список ограничений

opt = SolverFactory('ipopt')  # решаем их с помощью glpk
opt.solve_tsp(model)

print('Просто решение модели без ограничений')
model.display()

for i in range(5):
    expr = 0
    for j in model.x:
        if pyo.value(model.x[j]) < 0.5:
            expr += model.x[j]
        else:
            expr += (1 - model.x[j])
    model.cuts.add(expr >= 1)
    results = opt.solve_tsp(model)
    print("\n===== iteration", i)
    model.display()
