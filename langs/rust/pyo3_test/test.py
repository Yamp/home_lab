import union_find_py

print(vars(union_find_py))

a = union_find_py.UFForPython(10)
a.union(1, 2)
a.union(3, 4)
print(a.connected(1, 3))
print(a.connected(1, 300))
