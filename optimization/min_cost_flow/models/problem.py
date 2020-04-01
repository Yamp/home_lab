from dataclasses import dataclass
from pprint import pformat
from typing import Dict, List, Iterable, Tuple, Set

from optimization.min_cost_flow.models.basic_models import Node, Edge


@dataclass
class FlowProblem:
    nodes: Dict[Node, Node] = None
    edges: List[Edge] = None

    def __init__(self, nodes=Iterable[Node], edges=Iterable[Edge]):
        self.nodes = {n: n for n in nodes}
        self.edges = edges

    def __str__(self):
        return f'total_cost = {self.total_cost()}\n' + pformat(self.edges) + '\n\n' + pformat(self.nodes)

    def init_from_edge_data(self, edge_data: Iterable[Iterable], nodes: Dict[int, float]):
        """
        :param edge_data: List[(start, end, capacity, cost)]
        :param nodes: node_num -> supply
        :return: FlowSolution
        """
        self.edges = [Edge(*e) for e in edge_data]
        self.nodes = {}
        for i, s in nodes.items():
            n = Node(i, s)
            self.nodes[n] = n

        return self

    def init_from_google_like(
            self, start_nodes, end_nodes, capacities, unit_costs,
            supplies: Iterable[Tuple[int, float]]
    ):
        """
        Строим из данных в тупом формате гугла
        """
        self.init_from_edge_data(
            edge_data=zip(start_nodes, end_nodes, capacities, unit_costs),
            nodes={i: s for i, s in supplies}
        )

        return self

    def set_edges_from_solver(self, solver):
        self.edges = [
            Edge(
                start=solver.Tail(i),
                end=solver.Head(i),
                capacity=solver.Capacity(i),
                cost=solver.UnitCost(i),
                flow=solver.Flow(i),
            ) for i in range(solver.NumArcs())
        ]

    def sources(self) -> Set[object]:
        """ Вершины с положительным суплаем """
        return set(s.id for s in self.nodes if s.supply > 0)

    def destinations(self) -> Set[object]:
        """ Вершины с отрицательным суплаем """
        return set(s.id for s in self.nodes if s.supply < 0)

    def total_cost(self):
        """ Общая стоимость потока """
        return sum(e.flow * e.cost for e in self.edges)