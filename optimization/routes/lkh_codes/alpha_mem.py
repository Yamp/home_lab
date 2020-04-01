dad = [0] * 10  # предки текущей вершины
ROOT = 0
N = len(dad)

mark = [-1] * N  # будуший марк
b = [float('-inf')]
c = {}

for i in range(N):  # от каждой вершины (рассматриваем циклы через нее)
    k = i

    while k != ROOT:  # идем к корню
        par_k = dad[k]

        b[par_k] = max(b[k], c[k, par_k])  # b[родителя] = либо текущее ребро, либо то, что и так было

        mark[par_k] = i  # откуда мы пиздуем
        k = par_k

    for j in range(N):
        if j != i and mark[j] != i:
            parent_j = dad[j]
            b[j] = max(
                b[parent_j],
                c[j, parent_j]
            )
            # alpha = c[i, j] - b[j]
