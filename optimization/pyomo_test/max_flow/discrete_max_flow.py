import os
from itertools import product, chain
from pprint import pprint

from pyomo.core import base
from pyomo.core.kernel import objective
from pyomo.environ import *
import pyomo.environ as pyo
from typing import Dict, List, Tuple
import numpy as np

MAX_PRIORITY = 15
FOOLING_EDGES = 5
FAILURE_ID = -1834579344

# global vars
volume_sum = None


def print_result(res_dict):
    pprint(res_dict)


def normalize_volumes_and_capacities(volumes, capacities):
    """
    Гарантируем, что любой поток будет меньше 1 где угодно
    :param volumes: объемы в источниках
    :param capacities: вместимости ребер

    :return: new_volumes, new_capacities
    """
    global volume_sum

    volume_sum = sum(volumes.values())
    return (
        {k: v / volume_sum for k, v in volumes.items()} if volume_sum else {},
        {k: v / volume_sum for k, v in capacities.items()} if volume_sum else {},
    )


def normalize_prices(prices):
    """
    Любая цена меньше 1
    """
    return {
        k: v / max(prices.values())
        for k, v in prices.items()
    } if prices else {}


def discrete_min_cost_max_flow_model():
    """
    Создаем абстрактрую pyomo-модель, описывающую проблему и возвращаем ее
    """
    mod = base.AbstractModel()

    mod.sources = base.Set()  # источники
    mod.middles = base.Set()  # не источники
    mod.destinations = base.Set()  # стоки
    mod.non_source = mod.middles | mod.destinations
    mod.s2m = base.Set(within=mod.sources * mod.non_source)  # source -> non_source ребра
    mod.m2m = base.Set(within=mod.middles * mod.non_source)  # middle -> non_source ребра

    # Параметры модели
    mod.loss_fractions = base.Param(mod.middles, within=base.NonNegativeReals)  # количество отсортированной фракции
    mod.capacities = base.Param(mod.middles, within=base.NonNegativeReals)  # Вместимости вершин middles
    mod.prices_m2m = base.Param(mod.m2m, within=base.Reals)  # цены ребер m2m
    mod.prices_s2m = base.Param(mod.s2m, within=base.Reals)  # цены ребер s2m
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

    # суммарная рассчетная стоимость
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
    # общая потеря
    total_loss = lambda m: sum(in_flow(m, v) * m.loss_fractions[v] for v in m.middles)
    # поток выходящий из вершины vert -> все middle[dst]
    out_flow = lambda m, vert: sum(m.m2m_flows[src, dst] for src, dst in m.m2m if src == vert)

    # Из каждого источника выходит ровно одно ребро
    mod.one_x_constr = base.Constraint(
        mod.sources,
        rule=lambda m, vert: sum(
            m.s2m_indicators[src, dst] for src, dst in m.s2m if vert == src
        )
                             == 1,
    )

    # поток входящий в middle вершину не больше допустимого (мощности вершины)
    mod.capacity_constr = base.Constraint(
        mod.middles, rule=lambda m, v: in_flow(m, v) <= m.capacities[v]
    )

    # В сумме проталкиваем весь возможный поток
    # (поток входящий во все стоки - потери = sum поток выходящий из всех источников)
    mod.full_flow_constr = base.Constraint(
        rule=lambda m: total_flow(m) + total_loss(m) == sum(m.source_vol[s] for s in m.sources)
    )

    # поток входящий вершину равен выходящему
    mod.conservation_constr = base.Constraint(
        mod.middles,
        rule=lambda m, v: in_flow(m, v) * (1 - m.loss_fractions[v]) == out_flow(m, v),
    )

    # оптимизируем стоимость
    mod.total = base.Objective(sense=objective.minimize, rule=lambda m: total_cost(m))

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
        loss_fractions: Dict[int, float],  # отсортированная фракция
        priorities: Dict[Tuple[int, int], int]  # положительный приоритет уменьшает цену и наоборот
):
    sources_set, middles_set, dests_set = map(set, [sources, middles, destinations])
    non_source_set = middles_set | dests_set

    s2m = [e for e in edges if e[0] in sources_set and e[1] not in sources_set]
    m2m = [e for e in edges if e[0] in middles and e[1] in non_source_set]

    # тут стоимости потоков сразу с учетом потока!
    prices_s2m = {
        k: (prices[k] - np.sign(priorities[k]) * FOOLING_EDGES ** abs(priorities[k]))
           * source_vol[k[0]]
        for k in s2m
    }
    prices_m2m = {
        k: prices[k]  # если приоритет > 0 — цена уменьшается
           - np.sign(priorities[k]) * FOOLING_EDGES ** abs(priorities[k])
        for k in m2m
    }

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
        'loss_fractions': loss_fractions,
    }}

    return m.create_instance(data)


def get_solver():
    opt = pyo.SolverFactory("cbc")
    opt.options["threads"] = os.cpu_count()
    # opt.options['absmipgap'] = 1
    # mb ratioGap = 1%
    # seconds = 1000 sec?

    return opt


def add_fake_node(
        sources: List,
        edges: List[Tuple],
        destinations: List,
        prices: Dict[Tuple, float],
        priorities: Dict[Tuple, int],
):
    destinations += [FAILURE_ID]
    edges += [(s, FAILURE_ID) for s in sources]

    new_prices = {(s, FAILURE_ID): FOOLING_EDGES ** MAX_PRIORITY for s in sources}
    prices.update(new_prices)
    priorities.update({(s, FAILURE_ID): 0 for s in sources})


def solve(
        sources, middles, edges, capacities, destinations,
        prices, source_vol, loss_fractions, priorities
):
    """
    Решкалка: принимает все входные параметры, возвращает status и словарь потоков
    :return: status
    """
    prices = normalize_prices(prices)
    source_vol, capacities = normalize_volumes_and_capacities(source_vol, capacities)
    add_fake_node(
        sources=sources, edges=edges, destinations=destinations,
        prices=prices, priorities=priorities
    )
    instance = create_instance(
        m=discrete_min_cost_max_flow_model(),
        sources=sources, middles=middles, edges=edges,
        capacities=capacities, destinations=destinations,
        prices=prices, source_vol=source_vol, loss_fractions=loss_fractions,
        priorities=priorities
    )
    opt = get_solver()
    status = opt.solve(instance)

    return status, get_flows(instance)


def get_flows(instance):
    """
    Извлекаем результат, нормализуем обратно, потоки
    :param instance:
    :return:
    """
    global volume_sum
    res = {
        e: pyo.value(instance.m2m_flows[e])
        for e in instance.m2m_flows
    }

    res.update(
        {
            e: pyo.value(instance.s2m_indicators[e]) * pyo.value(instance.source_vol[e[0]])
            for e in instance.s2m_indicators
        }
    )

    # возвращаем к исходным единицам
    for k in res.keys():
        res[k] *= volume_sum

    return res


if __name__ == "__main__":
    def get_test_data(nodes):
        return nodes[:900], nodes[900:990], nodes[-10:]


    def get_small_test_data(nodes):
        return nodes[:7], nodes[8:10], nodes[10:11]


    nodes = list(range(1000))
    sources, middles, destinations = get_small_test_data(nodes)

    edges = [(i, j) for i, j in product(middles, middles + destinations) if i != j]
    edges += [(i, j) for i, j in product(sources, middles + destinations) if i != j]

    # приоритеты — целые числа
    # приоритет по умолчанию — 0, меньший приоритет — не писпользоват ребро, больший — обязательно использовать
    priorities = {(i, j): 0 for i, j in product(middles, middles + destinations) if i != j}
    priorities.update({(i, j): -1 for i, j in product(sources, middles + destinations) if i != j})

    loss_fractions = {i: 0.5 for i in middles}  # доля отсортировки
    capacities = {i: 3 for i in middles}
    prices = {(i, j): 1 for i, j in edges}
    source_vol = {i: 2 for i in sources}

    # print(f'{nodes=}\n{sources=}\n{middles=}\n{destinations=}\n{edges=}\n{capacities=}\n{prices=}\n{source_vol=}')

    status, res = solve(
        sources=sources, middles=middles, edges=edges,
        capacities=capacities, destinations=destinations,
        prices=prices, source_vol=source_vol, loss_fractions=loss_fractions,
        priorities=priorities
    )

    print(status)
    print_result(res)

    # TODO: ребра только в одну сторону (запретить поток из стока, веса любого знака)
