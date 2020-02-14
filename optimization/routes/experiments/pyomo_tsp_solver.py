import os
from itertools import product

from pyomo.core import base
from pyomo.core.kernel import objective
from pyomo.environ import *
from pyomo import opt as solvers
from typing import Dict, List, Tuple


def discreet_min_cost_max_flow_model():
    """
    Создаем абстрактрую pyomo-модель, описывающую проблему и возвращаем ее
    """
    mod = base.AbstractModel()

    mod.nodes = base.Set()  # источники
    mod.edges = base.Set(within=mod.nodes * mod.nodes)  # source -> middle ребра

    # Параметры модели
    mod.capacities = base.Param(mod.edges, within=base.NonNegativeReals)  # Вместимости вершин middles

    # Переменные
    mod.edge_indicators = base.Var(mod.edges, within=base.Boolean)  # индикаторы наличия потоков s2m

    def in_deg(m, vert):
        return sum(  # из middle[src] -> vert
            m.edge_indicators[src, dst]
            for src, dst in m.m2m
            if dst == vert
        )

    def out_deg(m, vert):
        return sum(  # из middle[src] -> vert
            m.edge_indicators[src, dst]
            for src, dst in m.m2m
            if src == vert
        )

    def total_cost(m):
        return \
            sum(
                m.m2m_flows[src, dst] * m.prices_m2m[src, dst]
                for src, dst in m.m2m
            ) + sum(
                m.s2m_indicators[src, dst] * m.prices_s2m[src, dst]  # тут стоимости потоков сразу с учетом потока!
                for src, dst in m.s2m
            )

    # поток приходящий в конечные вершины
    total_flow = lambda m: sum(in_deg(m, v) for v in m.destinations)
    # поток выходящий из вершины vert -> все middle[dst]
    out_flow = lambda m, vert: sum(m.m2m_flows[src, dst] for src, dst in m.m2m if src == vert)

    # Из каждого источника выходит ровно одно ребро
    mod.one_x_constr = base.Constraint(
        mod.nodes,
        rule=lambda m, vert: sum(m.s2m_indicators[src, dst] for src, dst in m.s2m if vert == src) == 1
    )

    # поток входящий в middle вершину не больше допустимого (мощности вершины)
    mod.capacity_constr = base.Constraint(
        mod.middles,
        rule=lambda m, v: in_deg(m, v) <= m.capacities[v]
    )

    # В сумме проталкиваем весь возможный поток
    mod.full_flow_constr = base.Constraint(
        rule=lambda m: total_flow(m) == sum(m.source_vol[s] for s in m.sources)
    )

    # поток входящий вершину равен выходящему
    mod.conservation_constr = base.Constraint(mod.middles, rule=lambda m, v: in_deg(m, v) == out_flow(m, v))

    mod.total = base.Objective(
        sense=objective.minimize,
        rule=lambda m: total_cost(m)
    )

    return mod
