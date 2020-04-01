from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Mapping, Set

from optimization.min_cost_flow.models.basic_models import Node, Edge
from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.solvers import BaseFlowSolver
from optimization.min_cost_flow.solvers.fast_flow_solver import FastFlowSolver


@dataclass
class DiscreteFlowApproximateSolver(BaseFlowSolver):
    """
    Запускаем min_cost_flow 1 раз
    Потом запускам его второй раз, но уменьшаем supplies образом, чтобы там было только количество,
    Которое утекает по самому жирному ребру (с самым большим потоком, можно другое какой-нибудь).
    Остальные ребра удаляем.

    @TODO: писал очень сонным, попроавить косяки
    """

    base_solver: 'BaseFlowSolver' = FastFlowSolver()  # TODO: dataclass
    problem: FlowProblem = None
    sources: Set = None
    residuals: Dict = None
    best_edges: Dict[Node, Edge] = None
    source_edges: Mapping[Node, List[Edge]] = None

    def solve(self, p: FlowProblem):
        self.base_solver.solve(p)
        self._source_edges(p)
        self._find_best_edges(p)

    def _source_edges(self, p: FlowProblem) -> None:
        self.sources = p.sources()
        self.source_edges = defaultdict(list)

        #  нашли все ребра
        for e in p.edges:
            if e.start in self.sources:
                self.source_edges[e.start] += [e]

    def _find_best_edges(self, p: FlowProblem):
        self.base_solver.solve(p)

        for s, edge_list in self.source_edges.items():
            best_edge = max(edge_list, key=lambda e: e.flow)
            self.residuals[s] = sum(e.flow for e in edge_list) - best_edge.flow
            self.best_edges[s] = best_edge

    def _fix_problem(self):
        new_edges = []

        for e in self.problem.edges:
            if e.start not in self.sources:  # ребра не от источников
                new_edges += [e]
            elif e in self.best_edges[e.start]:  # лучшие ребра от источников
                new_edges += [e]
                e.start.supply = e.flow
            else:
                continue


@dataclass
class IterativeRemoveSolver(BaseFlowSolver):
    """
    Cокращаем массу источника, потоки которого раздробились на массу потоков, ответвившихся от основного потока,
    запускаем тот же алгоритм заново
    если потоки от источников все еще дробятся, повторяем процедуру (скорее всего этот шаг не нужен)

    список потоков, причем потоки от источников не должны быть раздроблены
    список "потерянных масс" - список пар "id источника  -  значение массы, которая была исключена из потоков"

    Отбрасывать нужно не только немаксимальные потоки,
    но и соответственно снижать те потоки,
    которые получились из этих немаксимальных потоков дальше по графу
    @TODO
    """

    def solve(self, p: FlowProblem) -> FlowProblem:
        pass

    ...
