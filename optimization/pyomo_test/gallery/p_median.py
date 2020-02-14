from pyomo.environ import *
import random

model = AbstractModel()

# Количество кандидатов и точек
model.candidate_num, model.points_num = Param(within=PositiveIntegers), Param(within=PositiveIntegers)
# множества кандидатов и точек
model.candidates, model.points = RangeSet(1, model.candidate_num), RangeSet(1, model.points_num)

model.p = Param(within=RangeSet(1, model.candidate_num))  # количество медиан
model.demand = Param(model.points_num, default=1.0)  # спрос каждой точки
model.cost = Param(  # ценка каждой штуки
    model.candidates, model.points,
    initialize=lambda i, j, m: random.uniform(1.0, 2.0),
    within=Reals
)

# какая часть спроса точки удовлетворяется этим кандидатом
model.demand_frac = Var(model.M, model.N, bounds=(0.0, 1.0))
model.is_median = Var(model.candidate_num, within=Binary)  # выбираем ли эту точку медианой

# Опимизируемая функция
model.cost = Objective(
    rule=lambda m: sum(
        m.d[j] * m.cost[i, j] * m.x[i, j]
        for i in m.M
        for j in m.N
    )
)

# Ограничения
model.demand = Constraint(
    model.N,
    rule=lambda m, j: sum(m.x[i, j] for i in m.M) == 1
)

# ровно p центров
model.p_centers_constraint = Constraint(rule=lambda m: sum(model.y[i] for i in model.M) == model.p)

model.openfac = Constraint(
    model.M, model.N,
    rule=lambda m, i, j: m.x[i, j] <= m.y[i]
)
