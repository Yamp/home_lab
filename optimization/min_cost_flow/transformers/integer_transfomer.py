from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict

from optimization.min_cost_flow.models.basic_models import RestrictedNode, Node, Edge
from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.transformers import BaseTransformer


@dataclass
class IntegerTransformer(BaseTransformer):
    """
    Преобразует все значимые числа в проблеме в int для увеличения скорости решения
    Если у нас x64, возможно имеет смысл сделать точности ≈10^9
    """
    flow_limit: int = 10 ** 6  # максимальное число, чем больше, тем больше точность и вероятность переполнения
    cost_limit: int = 10 ** 6  # максимальное число, чем больше, тем больше точность и вероятность переполнения

    supply_sum: float = None
    max_cost: float = None

    saved_edges: Dict[Edge, Edge] = field(default_factory=dict)
    saved_nodes: Dict[Node, Node] = field(default_factory=dict)

    def transform(self, p: FlowProblem):
        self.supply_sum = sum(n.supply for n in p.nodes if n.supply > 0)
        self.max_cost = max(e.cost for e in p.edges)

        for e in p.edges:
            ecp = deepcopy(e)
            self.saved_edges[ecp] = ecp

            e.capacity = self._transform_flow(e.capacity)
            e.cost = int(e.cost / self.max_cost * self.cost_limit)

        for n in p.nodes:
            ncp = deepcopy(n)
            self.saved_nodes[ncp] = ncp

            n.supply = self._transform_flow(n.supply)
            if isinstance(n, RestrictedNode):
                n.capacity = self._transform_flow(n.capacity)

    def restore(self, p: FlowProblem):
        for e in p.edges:
            self._restore_edge(e)

        for k, v in p.nodes.items():
            restored = self._restore_node(k)
            p.nodes[k].__dict__.update(restored.__dict__)  # магия, чтобы у нас сохранились все ссылки

    # -------------------- Protected --------------------

    def _transform_flow(self, flow: float) -> int:
        """ Нормирует любые величины измеряемые в единицах потока """
        flow /= self.supply_sum
        flow = min(1.0, flow)  # не нужны capacity > суммы потока
        flow *= self.flow_limit

        return int(flow)

    def _transform_cost(self, cost: float) -> int:
        cost /= self.max_cost
        cost *= self.cost_limit  # не нужны capacity > суммы потока

        return int(cost)

    def _restore_flow(self, flow: float) -> float:
        return flow / self.flow_limit * self.supply_sum

    def _restore_edge(self, edge: Edge):
        edge.capacity = self.saved_edges[edge].capacity
        edge.cost = self.saved_edges[edge].cost
        edge.flow = self._restore_flow(edge.flow)
        edge.clip_flow()

    def _restore_node(self, node: Node):
        return self.saved_nodes[node]
