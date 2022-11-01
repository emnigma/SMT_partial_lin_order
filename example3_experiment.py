
from SMT_part_lin_order import SMT_part_lin_order


def main():

    n = 6  # elements
    A = {(0, 2), (1, 3), (2, 4), (3, 5), (2, 1), (5, 4)}

    s = SMT_part_lin_order(relations=A, n_elements=n)

    print(s.check())  # sat (ok)
    print(s.model())


if __name__ == "__main__":
    main()
