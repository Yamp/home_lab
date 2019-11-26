
from pyschedule import plotters, Scenario, solvers

S = Scenario('asdf', horizon=20)

r = S.Resource('r', periods=range(20))
t2 = S.Task('CE2', length=20)
t2 += r

res = solvers.mip.solve(S, msg=0)

print(S.solution())
print(S)
