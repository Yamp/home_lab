from copy import deepcopy
from dataclasses import dataclass
from typing import Dict

from bidict import bidict

from optimization.min_cost_flow.models.basic_models import Edge, RestrictedNode, Node
from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.transformers import BaseTransformer


@dataclass
class FictiousNode(Node):
    """ Класс-маркер того, что вершина не настоящая """
    real_node: RestrictedNode = None
    position: str = None

    def __init__(self, node: RestrictedNode, position: str):
        super().__init__(node.id, node.supply)

        self.position = position
        self.real_node = node


@dataclass
class FictiousEdge(Edge):
    """ Класс-маркер того, что ребро на самом деле заменяет RestrictedNode """
    real_node: RestrictedNode = None


@dataclass
class EliminateRestrictedTransformer(BaseTransformer):
    """
    Этот трансформер преобразует проблему с ограничениями на вершинах
    к обычной проблеме потоков с ограничениями на ребрах добавляя фиктивные ребра и вершины.
    """
    restricted2new: bidict = None
    old_nodes: Dict[Node, Node] = None

    # noinspection PyTypeChecker
    def transform(self, p: FlowProblem):
        self.old_nodes = deepcopy(p.nodes)

        new_edges = []
        new_nodes = {}
        replaced_nodes = {}

        # добавляем 2 новые вершины и фиктивное ребро
        for node in p.nodes:
            if isinstance(node, RestrictedNode):
                n_s, n_e, new_edge = self._build_new_edge(node)

                # сохраняем вершины и ребро
                new_nodes[n_s] = n_s
                new_nodes[n_e] = n_e
                new_edges += [new_edge]

                replaced_nodes[node] = new_edge  # сохраняем ребро, чтобы можно были извлечть начало и конец
            else:
                new_nodes[node] = node

        # Перестраиваем сломавшиеся из-за этого ребра
        for edge in p.edges:
            # если у ребра сломано начало, заменяем его на конец нового добавленного
            if edge.start in replaced_nodes:
                edge.start = replaced_nodes[edge.start].end

            # и наоборот
            if edge.end in replaced_nodes:
                edge.end = replaced_nodes[edge.end].start

        # Собственно обновляем нашу проблему
        p.nodes = new_nodes
        p.edges += new_edges

    def restore(self, p: FlowProblem):
        old_nodes, p.nodes = p.nodes, self.old_nodes  # восстанавливаем все старые вершины
        new_edges = []

        for edge in p.edges:
            if isinstance(edge, FictiousEdge):
                continue  # удаляем фиктивные ребра

            # меняем обратно начала и концы ребер
            if isinstance(edge.start, FictiousNode):
                edge.start = edge.start.real_node

            if isinstance(edge.end, FictiousNode):
                edge.end = edge.end.real_node

            new_edges += [edge]

        p.edges = new_edges

    # -------------------- protected --------------------

    def _build_new_edge(self, node: RestrictedNode):
        # новые вершины
        n_s = FictiousNode(node, position='start')
        n_e = FictiousNode(node, position='end')

        # новое ребро
        new_edge = FictiousEdge(
            start=n_s,
            end=n_e,
            capacity=float('+inf'),
            cost=0,
            real_node=node
        )

        return n_s, n_e, new_edge
