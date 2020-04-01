from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.solvers import BaseFlowSolver
from optimization.min_cost_flow.solvers.google_or_solver import GoogleOrFlowSolver
from optimization.min_cost_flow.solvers.transformative_solver import TransformationalSolver
from optimization.min_cost_flow.transformers.eliminate_restricted_transformer import EliminateRestrictedTransformer
from optimization.min_cost_flow.transformers.integer_transfomer import IntegerTransformer


class FastFlowSolver(BaseFlowSolver):
    """
    Оптимальный солвер, который использует google-or и все улучшающие трансформеры
    """
    def __init__(self):
        self._solver = TransformationalSolver(
            transformers=[
                EliminateRestrictedTransformer(),
                IntegerTransformer(),
            ],
            basic_solver=GoogleOrFlowSolver()
        )

    def solve(self, p: FlowProblem) -> FlowProblem:
        return self._solver.solve(p)
