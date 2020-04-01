from dataclasses import dataclass, field
from typing import Dict

from bidict import bidict

from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.transformers import BaseTransformer


# noinspection PyProtectedMember
@dataclass
class EnumerateTransformer(BaseTransformer):
    """
    Трансформер, который заменяет id на последовательные номера int и обратно
    По возможности должен быть последним в списке трансформеров
    """
    int_id_2_node: bidict = field(default_factory=bidict)
    int_id_2_node_id: Dict = field(default_factory=bidict)

    def transform(self, p: FlowProblem):
        for i, n in enumerate(p.nodes):
            self.int_id_2_node[i] = n

        for e in p.edges:
            e.start = self.int_id_2_node.inverse[e.start]
            e.end = self.int_id_2_node.inverse[e.end]

        for i, n in enumerate(p.nodes):
            self.int_id_2_node_id[i] = n.id
            n._id = i

    def restore(self, p: FlowProblem):
        for i, n in enumerate(p.nodes):
            n._id = self.int_id_2_node_id[n._id]  # ресторим id

        for e in p.edges:
            e.start = self.int_id_2_node[e.start]
            e.end = self.int_id_2_node[e.end]
