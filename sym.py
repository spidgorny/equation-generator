import sympy
from sympy import symbols, init_printing, solveset, Eq, linsolve, Symbol, EmptySet
import random

from sympy.logic.boolalg import BooleanFalse

init_printing(use_unicode=True)


def getEq(x: Symbol):
    range = 100
    a = random.randint(-range, range)
    b = random.randint(-range, range)
    c = random.randint(-range, range)
    eq1 = Eq(a * x + b, c)
    return eq1


def genEq2(x: Symbol, y: Symbol):
    while True:
        try:
            eq1 = getEq(x)
            eq2 = getEq(y)
            print('⎧ ', eq1)
            print('⎨')
            print('⎩ ', eq2)
            res = linsolve([eq1, eq2], [x, y])
        except AttributeError:
            res = EmptySet
        if not (res is EmptySet) and not (res is BooleanFalse):
            return eq1, eq2


def solve(eq1, eq2, x, y):
    res = linsolve([eq1, eq2], [x, y])
    print(res)
    return res


def getSimpleEq2(x: Symbol, y: Symbol):
    while True:
        eq1, eq2 = genEq2(x, y)
        res = solve(eq1, eq2, x, y)
        val_x = tuple(res)[0][0]
        val_y = tuple(res)[0][1]
        print(type(val_x), type(val_y))
        rat = 1 if isinstance(val_x, sympy.core.numbers.Integer) else 0
        rat += 1 if isinstance(val_y, sympy.core.numbers.Integer) else 0
        if rat > 0:
            return eq1, eq2
        continue


if __name__ == '__main__':
    x, y = symbols('x y')
    # eq1, eq2 = genEq2(x, y)
    eq1, eq2 = getSimpleEq2(x, y)
    solve(eq1, eq2, x, y)
