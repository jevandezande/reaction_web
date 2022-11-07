from itertools import product


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
B, 1, {r1}, {r2}, {r3}, {r4}, {r5}, {e2}
C, 1, {r1}, {r2}, {r3}, {r4}, {r5}, {e3}
D, 1, {r1}, {r2}, {r3}, {r4}, {r5}, {e4 + e5}
"""
        for (r1, e1), (r2, e2), (r3, e3), (r4, e4), (r5, e5) in product(*r_groups.values())
    )

    return header + data.strip()


if __name__ == "__main__":
    with open("enum_2_3_2_3_4.csv", "w") as f:
        f.write(gen_enumeration())
