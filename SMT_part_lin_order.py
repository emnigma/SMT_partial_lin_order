
import typing as tp
from z3 import *


def SMT_part_lin_order(relations: tp.Set, n_elements: int) -> Solver:

    n = n_elements
    A = relations

    vars = [Bool(f"var_{i}") for i in range(n)]
    A = {(vars[i1], vars[i2]) for (i1, i2) in A}

    # R(int, int) -> bool, если я правильно понимаю
    R = Function('R', IntSort(), IntSort(), BoolSort())

    s = Solver()

    # добавить все отношения из условия в Solver
    for (v1, v2) in A:
        s.add(R(v1, v2))

    # посмотрел вот тут: https://theory.stanford.edu/~nikolaj/programmingz3.html#sec-transitive-closure
    TC_R = TransitiveClosure(R)

    # добавить условие на транзитивное замыкание
    for relation1 in A:
        a1, b1 = relation1
        for relation2 in A:
            a2, b2 = relation2
            # what if (a, b), (b, a)?
            s.add(
                Implies(
                    And(b1 == a2, a1 != b2),
                    TC_R(a1, b2)
                )
            )

    # 3: antisymmetric
    for v1 in vars:
        for v2 in vars:
            s.add(
                Implies(
                    And(R(v1, v2), R(v2, v1)),
                    v1 == v2
                )
            )

    return s
