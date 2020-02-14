import numpy as np
import scipy.sparse as sp
from cylp.cy import CyClpSimplex
np.random.seed(1)

""" INSTANCE """
weight = np.random.randint(10, size = 1000)
value = np.random.randint(10, size = 1000)
capacity = 500

""" SOLVE """
n = weight.shape[0]
model = CyClpSimplex()
x = model.addVariable('x', n, isInt=True)
model.objective = -value
model += sp.eye(n) * x >= np.zeros(n)  # could be improved
model += sp.eye(n) * x <= np.ones(n)   # """
model += np.matrix(weight) * x <= capacity  # cylp somewhat outdated in terms of np-usage!
cbcModel = model.getCbcModel()  # Clp -> Cbc model / LP -> MIP
cbcModel.logLevel = True
status = cbcModel.solve_tsp()
x_sol = np.array(cbcModel.primalVariableSolution['x'].round()).astype(int)  # assumes there is one

print(x_sol)
print(x_sol.dot(weight))
print(x_sol.dot(value))
