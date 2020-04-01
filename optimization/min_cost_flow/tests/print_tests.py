from typing import List

from optimization.min_cost_flow.models.basic_models import Edge, Node
from optimization.min_cost_flow.models.problem import FlowProblem
from optimization.min_cost_flow.solvers.fast_flow_solver import FastFlowSolver
from optimization.min_cost_flow.solvers.google_or_solver import GoogleOrFlowSolver


def test_google():
    start_nodes = [0, 0, 1, 1, 1, 2, 2, 3, 4]
    end_nodes = [1, 2, 2, 3, 4, 3, 4, 4, 2]
    capacities = [15, 8, 20, 4, 10, 15, 4, 20, 5]
    unit_costs = [4, 4, 2, 2, 6, 1, 3, 2, 3]
    supplies: List[int] = [20, 0, 0, -5, -15]

    solver = GoogleOrFlowSolver()
    # noinspection PyTypeChecker
    problem = FlowProblem().init_from_google_like(
        start_nodes=start_nodes,
        end_nodes=end_nodes,
        capacities=capacities,
        unit_costs=unit_costs,
        supplies=enumerate(supplies),
    )

    print(solver.solve(problem))


def test_edges():
    nodes = [Node('my_ind ' + str(i), s) for i, s in enumerate([20, 0, 0, -5, -15])]
    edges = [
        Edge(start=nodes[0], end=nodes[1], capacity=15, cost=4),
        Edge(start=nodes[0], end=nodes[2], capacity=8, cost=4),
        Edge(start=nodes[1], end=nodes[2], capacity=20, cost=2),
        Edge(start=nodes[1], end=nodes[3], capacity=4, cost=2),
        Edge(start=nodes[1], end=nodes[4], capacity=10, cost=6),
        Edge(start=nodes[2], end=nodes[3], capacity=15, cost=1),
        Edge(start=nodes[2], end=nodes[4], capacity=4, cost=3),
        Edge(start=nodes[3], end=nodes[4], capacity=20, cost=2),
        Edge(start=nodes[4], end=nodes[2], capacity=5, cost=3),
    ]
    problem = FlowProblem(edges=edges, nodes=nodes)
    solver = FastFlowSolver()

    print(solver.solve(problem))


if __name__ == '__main__':
    # test_google()
    test_edges()
