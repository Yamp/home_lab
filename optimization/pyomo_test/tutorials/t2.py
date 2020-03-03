# iterative1.py
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Create a solver
opt = pyo.SolverFactory("glpk")

#
# A simple model with binary variables and
# an empty constraint list.
#
model = pyo.AbstractModel()
model.n = pyo.Param(default=4)
model.x = pyo.Var(pyo.RangeSet(model.n), within=pyo.Binary)


def o_rule(model):
    return pyo.summation(model.x)


def solve_and_print(model):
    results = opt.solve_tsp(instance)
    instance.display()


model.o = pyo.Objective(rule=o_rule)  # добавляем цел оптимзации в виде функции
model.c = pyo.ConstraintList()  # создаем пустой список огрангичений

print('Создаем конкретную модель из абстрактной и решаем')
instance = model.create_instance(,
solve_and_print(instance)

# Iterate to eliminate the previously found solution
for i in range(5):
    print('!' * 100, f'Итерация {i}', '!' * 100, sep='\n')
    expr = 0
    for j in instance.x:
        if pyo.value(instance.x[j]) == 0:
            expr += instance.x[j]
        else:
            expr += 1 - instance.x[j]
    instance.c.add(expr >= 1)
    solve_and_print(instance)
