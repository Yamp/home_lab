from dataclasses import dataclass

from ortools.graph import pywrapgraph

from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.solvers import BaseFlowSolver
from optimization.min_cost_flow.solvers.transformative_solver import BaseTransformationalSolver
from optimization.min_cost_flow.transformers.enumerate_ransformer import EnumerateTransformer
from optimization.min_cost_flow.transformers.integer_transfomer import IntegerTransformer


class GoogleOrFlowSolver(BaseTransformationalSolver):
    """
    Решает задачу min_cost_flow при помощи библиотеки google-or
    """

    def __init__(self):
        self.transformers = [EnumerateTransformer()]

    def basic_solve(self, p: FlowProblem):
        """ Решаем min cost flow с помощью google-or солвера """
        or_solver = pywrapgraph.SimpleMinCostFlow()

        # Добавляем ребра
        for e in p.edges:
            or_solver.AddArcWithCapacityAndUnitCost(e.start, e.end, e.capacity, e.cost)

        # добавляем начальные количества
        for s in p.nodes:
            or_solver.SetNodeSupply(s.id, s.supply)

        # возвращаем решение
        status = or_solver.Solve()
        if status != or_solver.OPTIMAL:
            raise ValueError(f'Not solved to optimality! {status}')
        else:
            p.set_edges_from_solver(or_solver)

        return p
