
import typing as tp
from z3 import *


def SMT_part_lin_order(relations: tp.Set, n_elements: int) -> Solver:

    n = n_elements
    A = relations

    vars = [IntVal(i) for i in range(n)]
    A = {(vars[i1], vars[i2]) for (i1, i2) in A}

    # R(int, int) -> bool, если я правильно понимаю
    R = Function('R', IntSort(), IntSort(), BoolSort())

    s = Solver()

    # добавил все отношения из условия в Solver
    for (v1, v2) in A:
        s.add(R(v1, v2))

    # условие на рефлексивность:
    for v in vars:
        if (v, v) not in A:
            s.add(R(v, v))

    # добавил условие на транзитивное замыкание
    # i, j, k from vars => (iRj and jRk => iRk)
    for relation1 in A:
        a1, b1 = relation1
        for relation2 in A:
            a2, b2 = relation2
            s.add(
                Implies(
                    # b1 == a2: средние элементы равны (?, j), (j, ?)
                    # a1 != b2: крайние элементы не одинаковы (v1, j), (j, v2)
                    And(b1 == a2, a1 != b2),
                    R(a1, b2)
                )
            )

    core_var_num = 0
    # 3: antisymmetric
    for v1 in vars:
        for v2 in vars:
            core_var = Bool(f"core_var_{core_var_num}")
            core_var_num += 1
            s.assert_and_track(
                Implies(
                    And(R(v1, v2), R(v2, v1)),
                    v1 == v2
                ), core_var
            )
            # s.add(
            #     Implies(
            #         And(R(v1, v2), R(v2, v1)),
            #         v1 == v2
            #     )
            # )

    return s
