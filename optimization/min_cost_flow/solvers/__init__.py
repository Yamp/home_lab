from abc import abstractmethod
from dataclasses import dataclass

from optimization.min_cost_flow.models.problem import FlowProblem


@dataclass
class BaseFlowSolver:
    @abstractmethod
    def solve(self, p: FlowProblem) -> FlowProblem:
        return p
