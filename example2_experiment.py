from SMT_part_lin_order import SMT_part_lin_order


def main():

    n = 5  # elements
    A = {(0, 1), (2, 3), (3, 4), (4, 2)}

    s = SMT_part_lin_order(relations=A, n_elements=n)

    print(s.check())  # unsat (ok)
    # print(s.model())
    print(s.unsat_core())


if __name__ == "__main__":
    main()
