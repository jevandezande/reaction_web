import pandas as pd

from reaction_web.tools.generate_paths import find_r_groups, read_csv, read_multipath_csv


def test_read_csv():
    e_data = read_csv("tests/tools/data.csv", energy="e_energy")
    g_data = read_csv("tests/tools/data.csv", energy="gibbs_energy")

    assert len(e_data) == len(g_data)

    for mol_e, mol_g in zip(e_data, g_data):
        assert mol_e.name == mol_g.name

    assert e_data[0].energy == g_data[0].energy - 0.1


def test_read_multipath_csv():
    e_data = read_multipath_csv("tests/tools/data.csv", energy="e_energy")
    g_data = read_multipath_csv("tests/tools/data.csv", energy="gibbs_energy")

    assert len(e_data) == len(g_data)

    for path_e, path_g in zip(e_data.values(), g_data.values()):
        assert path_e.name == path_g.name
        assert len(path_e) == len(path_g)
        assert all(
            (rxn_e.reactants[0].name == rxn_g.reactants[0].name) and (rxn_e.products[0].name == rxn_g.products[0].name)
            for rxn_e, rxn_g in zip(path_e, path_g)
        )


def test_find_r_groups():
    r_groups = [f"r{i}" for i in range(8)]
    df = pd.DataFrame([[0] * 10], columns=["name"] + r_groups[:5] + ["step"] + r_groups[5:])
    assert find_r_groups(df) == r_groups
