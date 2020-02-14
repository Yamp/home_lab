from pyomo.environ import *


def flow_conservation(m, k: int):
    if k == value(m.source) or k == value(m.sink):
        return Constraint.Skip

    in_, out_ = 0, 0
    for i, j in m.edges:
        if i == k:
            in_ += m.flow[i, j]
        if j == k:
            out_ += m.flow[i, j]

    return in_ == out_


# Множества
model = AbstractModel()
model.nodes = Set()
model.edges = Set(within=model.nodes * model.nodes)

# Параметры модели
model.source = Param(within=model.nodes)  # Источник
model.sink = Param(within=model.nodes)  # Сток
model.capacity = Param(model.edges)  # Вместимости ребер

# Переменные
model.flow = Var(model.edges, within=NonNegativeReals)  # потоки по каждому ребру (уже не отрицательные)

# Суммарный поток в сток — цель оптимизации
model.total = Objective(
    rule=lambda m: sum(model.flow[i, j] for i, j in model.edges if j == value(model.sink)),
    sense=maximize
)

# Ограничения
model.capacity_constr = Constraint(
    model.edges,
    rule=lambda m, i, j: m.flow[i, j] <= m.capacity[i, j]  # вместимость ребра
)

model.conservation_constr = Constraint(model.nodes, rule=flow_conservation)  # сохранение потока через вершмну
