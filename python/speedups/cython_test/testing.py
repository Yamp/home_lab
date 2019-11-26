# from speedups.cython_test.dep import example_cy

import timeit

cy = timeit.timeit('example_cy.test(1000)', setup='import example_cy', number=10000)
py = timeit.timeit('example_py.test(1000)', setup='import example_py', number=10000)

print(cy, py)
print(f'Cy is {py / cy} times faster')
