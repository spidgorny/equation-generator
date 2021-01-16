from sympy import symbols, init_printing, solveset, Eq, linsolve, Symbol, EmptySet
import random

from sympy.logic.boolalg import BooleanFalse

init_printing(use_unicode=True)


def genEq2(x: Symbol, y: Symbol):
    while True:
        try:
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            eq1 = Eq(a * x + b, c)
            a2 = random.randint(-10, 10)
            b2 = random.randint(-10, 10)
            c2 = random.randint(-10, 10)
            eq2 = Eq(a2 * y + b2, c2)
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


if __name__ == '__main__':
    x, y = symbols('x y')
    eq1, eq2 = genEq2(x, y)
    solve(eq1, eq2, x, y)
