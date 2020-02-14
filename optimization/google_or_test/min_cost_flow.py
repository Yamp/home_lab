
# ребра и их характеристики
from ortools.graph import pywrapgraph

start_nodes = [0, 0, 1, 1, 1, 2, 2, 3, 4]
end_nodes = [1, 2, 2, 3, 4, 3, 4, 4, 2]
capacities = [15, 8, 20, 4, 10, 15, 4, 20, 5]
unit_costs = [4, 4, 2, 2, 6, 1, 3, 2, 3]

# supply в каждой вершине
supplies = [20, 0, 0, -5, -15]


min_cost_flow = pywrapgraph.SimpleMinCostFlow()

for i in range(0, len(start_nodes)):
    min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i], capacities[i], unit_costs[i])
