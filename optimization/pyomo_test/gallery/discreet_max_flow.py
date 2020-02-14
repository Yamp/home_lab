import os
from itertools import product

from pyomo.core import base
from pyomo.core.kernel import objective
from pyomo.environ import *
from pyomo import opt as solvers
from typing import Dict, List, Tuple


PRICE_OF_FAILURE = 10 ** 7
FAILURE_ID = -1834579344


def print_result(model):
    # print(f'Статус = {status.solver.termination_condition}')
    model.display()


def discreet_min_cost_max_flow_model():
    """
    Создаем абстрактрую pyomo-модель, описывающую проблему и возвращаем ее
    """
    mod = base.AbstractModel()

    mod.sources = base.Set()  # источники
    mod.middles = base.Set()  # не источники
    mod.destinations = base.Set()  # стоки
    mod.non_source = mod.middles | mod.destinations
    mod.s2m = base.Set(within=mod.sources * mod.non_source)  # source -> middle ребра
    mod.m2m = base.Set(within=mod.middles * mod.non_source)  # middle -> middle ребра

    # Параметры модели
    mod.capacities = base.Param(mod.middles, within=base.NonNegativeReals)  # Вместимости вершин middles
    mod.prices_m2m = base.Param(mod.m2m, within=base.NonNegativeReals)  # цены ребер m2m
    mod.prices_s2m = base.Param(mod.s2m, within=base.NonNegativeReals)  # цены ребер s2m
    mod.source_vol = base.Param(mod.sources, within=base.NonNegativeReals)  # количество потока рождаемого в источнике

    # Переменные
    mod.s2m_indicators = base.Var(mod.s2m, within=base.Boolean)  # индикаторы наличия потоков s2m
    mod.m2m_flows = base.Var(mod.m2m, within=base.NonNegativeReals)  # потоки по каждому m2m (уже неотрицательные)

    # поток входящий вершину (m2m + s2m)
    def in_flow(m, vert):
        return \
            sum(  # из middle[src] -> vert
                m.m2m_flows[src, dst]
                for src, dst in m.m2m
                if dst == vert
            ) + sum(  # из source[src] -> vert
                m.s2m_indicators[src, dst] * m.source_vol[src]
                for src, dst in m.s2m
                if dst == vert
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
    total_flow = lambda m: sum(in_flow(m, v) for v in m.destinations)
    # поток выходящий из вершины vert -> все middle[dst]
    out_flow = lambda m, vert: sum(m.m2m_flows[src, dst] for src, dst in m.m2m if src == vert)

    # Из каждого источника выходит ровно одно ребро
    mod.one_x_constr = base.Constraint(
        mod.sources,
        rule=lambda m, vert: sum(m.s2m_indicators[src, dst] for src, dst in m.s2m if vert == src) == 1
    )

    # поток входящий в middle вершину не больше допустимого (мощности вершины)
    mod.capacity_constr = base.Constraint(
        mod.middles,
        rule=lambda m, v: in_flow(m, v) <= m.capacities[v]
    )

    # В сумме проталкиваем весь возможный поток
    mod.full_flow_constr = base.Constraint(
        rule=lambda m: total_flow(m) == sum(m.source_vol[s] for s in m.sources)
    )

    # поток входящий вершину равен выходящему
    mod.conservation_constr = base.Constraint(mod.middles, rule=lambda m, v: in_flow(m, v) == out_flow(m, v))

    mod.total = base.Objective(
        sense=objective.minimize,
        rule=lambda m: total_cost(m)
    )

    return mod


def create_instance(
        m,
        sources: List[int],  # id вершин
        middles: List[int],
        destinations: List[int],  # список id стоков

        edges: List[Tuple[int, int]],  # допустимые ребра
        capacities: Dict[int, float],  # словарь вершина -> пропускная способность
        prices: Dict[Tuple, float],  # (v2, v2) -> цена на единицук потока
        source_vol: Dict[int, float],  # индекс источника -> генерируемый поток
):
    sources_set, middles_set, dests_set = map(set, [sources, middles, destinations])
    non_source_set = middles_set | dests_set

    s2m = [e for e in edges if e[0] in sources_set and e[1] not in sources_set]
    m2m = [e for e in edges if e[0] in middles and e[1] in non_source_set]

    # тут стоимости потоков сразу с учетом потока!
    prices_s2m = {k: prices[k] * source_vol[k[0]] for k in s2m}
    prices_m2m = {k: prices[k] for k in m2m}

    data = {None: {
        # Множества
        'sources': {None: sources},
        'middles': {None: middles},
        'destinations': {None: destinations},
        's2m': {None: s2m},
        'm2m': {None: m2m},

        # Параметры
        'capacities': capacities,
        'prices_m2m': prices_m2m,
        'prices_s2m': prices_s2m,
        'source_vol': source_vol,
    }}

    return m.create_instance(data)


def get_solver():
    opt = solvers.SolverFactory('cplex')
    opt.options['threads'] = os.cpu_count()
    # opt.options['absmipgap'] = 1
    # mb ratioGap = 1%
    # seconds = 1000 sec?

    return opt


def add_fake_node(sources, edges, destinations, prices):
    destinations += [FAILURE_ID]
    edges += [(s, FAILURE_ID) for s in sources]

    new_prices = {(s, FAILURE_ID): PRICE_OF_FAILURE for s in sources}
    prices.update(new_prices)


def solve(sources, middles, edges, capacities, destinations, prices, source_vol):
    add_fake_node(sources, edges, destinations, prices)
    model = discreet_min_cost_max_flow_model()
    instance = create_instance(
        m=model,
        sources=sources, middles=middles, edges=edges,
        capacities=capacities, destinations=destinations,
        prices=prices, source_vol=source_vol
    )
    opt = get_solver()
    status = opt.solve_tsp(instance)

    return status, instance


if __name__ == "__main__":
    # тестовые данные
    nodes = list(range(1000))
    sources = nodes[:900]
    middles = nodes[900:990]
    destinations = nodes[-10:]

    edges = [(i, j) for i, j in product(middles, middles + destinations) if i != j]
    edges += [(i, j) for i, j in product(sources, middles) if i != j]
    # edges.remove((0, 9))
    capacities = {i: 3 for i in middles}
    prices = {(i, j): 1 for i, j in edges}
    source_vol = {i: 2 for i in sources}

    # print(f'{nodes=}\n{sources=}\n{middles=}\n{destinations=}\n{edges=}\n{capacities=}\n{prices=}\n{source_vol=}')

    status, res = solve(sources=sources, middles=middles, edges=edges,
                        capacities=capacities, destinations=destinations,
                        prices=prices, source_vol=source_vol)

    print(status)
    # print_result(res)

    # TODO: ребра только в одну сторону (запретить поток из стока, веса любого знака)
