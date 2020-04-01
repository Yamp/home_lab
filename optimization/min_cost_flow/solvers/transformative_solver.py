from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterable, List

from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.solvers import BaseFlowSolver
from optimization.min_cost_flow.transformers import BaseTransformer


@dataclass
class BaseTransformationalSolver(BaseFlowSolver, BaseTransformer):
    """
    Применяет все трансформы до и откатывает после решения.
    Должен реализовать функцию basic_solve в которой будет сам алгоритм решения
    """
    transformers: List[BaseTransformer]

    def transform(self, p: FlowProblem):
        for t in self.transformers:
            t.transform(p)

    def restore(self, p: FlowProblem):
        for t in reversed(self.transformers):
            t.restore(p)

    def solve(self, p: FlowProblem) -> FlowProblem:
        self.transform(p)
        self.basic_solve(p)
        self.restore(p)

        return p

    @abstractmethod
    def basic_solve(self, p: FlowProblem):
        pass


@dataclass
class TransformationalSolver(BaseTransformationalSolver):
    """ Применяет все трансформы и рещает min_cost базовым солвером """
    basic_solver: BaseFlowSolver

    def basic_solve(self, p: FlowProblem):
        self.basic_solver.solve(p)
