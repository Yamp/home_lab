from z3 import *

print('--------------------------------- EXAMPLE 1 -------------------------------------------------------------')

Tie, Shirt = Bools('Tie Shirt')
s = Solver()
s.add(Or(Tie, Shirt),
      Or(Not(Tie), Shirt),
      Or(Not(Tie), Not(Shirt)))
print(s.check())
print(s.model())

print('--------------------------------- EXAMPLE 2 -------------------------------------------------------------')

Z = IntSort()
f = Function('f', Z, Z)
x, y, z = Ints('x y z')
A = Array('A', Z, Z)
fml = Implies(x + 2 == y, f(Store(A, x, 3)[y - 2]) == f(y - x + 1))
solve(Not(fml))

print('--------------------------------- EXAMPLE 3 -------------------------------------------------------------')

B = BoolSort()
f = Function('f', B, Z)
g = Function('g', Z, B)
a = Bool('a')
solve(g(1 + f(a)))

print('--------------------------------- EXAMPLE 4 -------------------------------------------------------------')

x, y = Ints('x y')
n = x + y >= 3
print("num args: ", n.num_args())
print("children: ", n.children())
print("1st child:", n.arg(0))
print("2nd child:", n.arg(1))
print("operator: ", n.decl())
print("op name:  ", n.decl().name())

print('--------------------------------- EXAMPLE 5 -------------------------------------------------------------')

solve([y == x + 1, ForAll([y], Implies(y <= 0, x < y))])

print('--------------------------------- EXAMPLE 6 -------------------------------------------------------------')

m, m1 = Array('m', Z, Z), Array('m1', Z, Z)
# можно фигачить нормальные такие лямбды
memset = lambda lo, hi, y, m: Lambda([x], If(And(lo <= x, x <= hi), y, Select(m, x)))
solve([m1 == memset(1, 700, z, m), Select(m1, 6) != z])

print('--------------------------------- EXAMPLE 7 -------------------------------------------------------------')

Q = Array('Q', Z, B)
prove(
    Implies(
        ForAll(Q,
               Implies(Select(Q, x), Select(Q, y))),
        # --------------------------- ==> ---------------------------
        x == y
    )
)

print('--------------------------------- EXAMPLE 8 -------------------------------------------------------------')

f = Function('f', Z, Z)
x = Const('x', Z)
print('Простой кейс')
# solve(
#     ForAll(
#         x,
#         f(f(x)) == x
#     ),
#     ForAll(
#         x,
#         f(f(f(x))) == x
#     )
# )
solve(f(f(x)) == x, f(f(f(x))) == x)
print('Сложнее')
solve(
    ForAll(
        x,
        f(f(x)) == x
    ),
    ForAll(
        x,
        f(f(f(x))) == x
    ),
    f(x) != x
)
print('Из олимпиады')

s = Solver()
s.add( 
    And(
        ForAll(
            x,
            f(f(x)) == x
        ),
        ForAll(
            x,
            f(f(x + 2) + 2) == x,
        ),
        f(0) == 1,
        ForAll(  # Exists
            x,
            f(x) != 1 - x
        )
    )
)
print(s.check())
# print(s.model())
