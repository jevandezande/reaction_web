import random
from itertools import product
from string import ascii_lowercase, ascii_uppercase

from more_itertools import take


def gen_enumeration():
    r_groups = {
        "r1": (("A", 1), ("B", 2)),
        "r2": (("C", 1), ("D", 3), ("E", 7)),
        "r3": (("F", 1), ("G", 4)),
        "r4": (("H", 1), ("I", 5), ("J", 8)),
        "r5": (("K", 1), ("L", 6), ("M", 9), ("N", 10)),
    }
    # shape = (2, 3, 2, 3, 4)

    header = "name, step, r1, r2, r3, r4, r5, energy\n"
    data = "".join(
        f"""\
A, 1, {r1}, {r2}, {r3}, {r4}, {r5}, {e1}
B, 2, {r1}, {r2}, {r3}, {r4}, {r5}, {e2}
C, 3, {r1}, {r2}, {r3}, {r4}, {r5}, {e3}
D, 4, {r1}, {r2}, {r3}, {r4}, {r5}, {e4 + e5}
"""
        for (r1, e1), (r2, e2), (r3, e3), (r4, e4), (r5, e5) in product(*r_groups.values())
    )

    return header + data.strip()


def gen_enumeration_from_shape(r_shape: tuple[int, ...], num_steps: int = 5, seed: int | None = None):
    """
    Programmatically generate an enumeration for testing purposes.

    :param r_shape: shape of the r_groups
    :param num_steps: number of steps in the Paths
    :param seed: random seed for energies
    """
    if seed:
        random.seed(seed)

    header = "name, step, " + ", ".join(f"r{i}" for i in range(len(r_shape))) + ", energy\n"

    molecules = ascii_lowercase[:num_steps]
    r_group_it = iter(ascii_uppercase)
    r_groups = [take(size, r_group_it) for size in r_shape]

    return header + "\n".join(
        "\n".join(
            f"{mol}, {step}, " + ", ".join(r_group_set) + f", {random.randint(0, 10)}"
            for step, mol in enumerate(molecules)
        )
        for r_group_set in product(*r_groups)
    )


if __name__ == "__main__":
    with open("enum_2_3_2_3_4.csv", "w") as f:
        f.write(gen_enumeration())

    with open("enum_3_4_3.csv", "w") as f:
        f.write(gen_enumeration_from_shape((3, 4, 3), num_steps=4, seed=42))
