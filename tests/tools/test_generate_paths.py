"""Tests for the generate_paths module."""

import pandas as pd
from pytest import mark

from reaction_web import Enumeration
from reaction_web.tools.generate_paths import (
    enumeration_factory,
    find_r_groups,
    read_csv,
    read_multipath_csv,
)


def test_read_csv() -> None:
    """Test reading a csv file with a single energy column."""
    e_data = read_csv("tests/data/enum_2_3.csv", energy="e_energy")
    g_data = read_csv("tests/data/enum_2_3.csv", energy="gibbs_energy")

    assert len(e_data) == len(g_data)

    for mol_e, mol_g in zip(e_data, g_data):
        assert mol_e.name == mol_g.name

    assert e_data[0].energy == g_data[0].energy - 0.1

    data2 = read_csv("tests/data/enum_2_2_2.csv")
    assert len(data2) == 16


def test_read_multipath_csv() -> None:
    """Test reading a csv file with multiple paths."""
    e_paths_dict, e_pi_dict = read_multipath_csv("tests/data/enum_2_3.csv", energy="e_energy")
    g_paths_dict, g_pi_dict = read_multipath_csv(
        "tests/data/enum_2_3.csv", energy="gibbs_energy", path_indicators=["r1", "r2"]
    )

    assert len(e_paths_dict) == len(g_paths_dict)
    assert e_pi_dict == g_pi_dict

    for path_e, path_g in zip(e_paths_dict.values(), g_paths_dict.values()):
        assert path_e.name == path_g.name
        assert len(path_e) == len(path_g)
        assert all(
            (rxn_e.reactants[0].name == rxn_g.reactants[0].name) and (rxn_e.products[0].name == rxn_g.products[0].name)
            for rxn_e, rxn_g in zip(path_e, path_g)
        )

    paths_dict, pi_dict = read_multipath_csv("tests/data/enum_2_2_2.csv")
    assert len(paths_dict) == 8
    assert len(pi_dict) == 3


def test_find_r_groups() -> None:
    """Test finding the r groups in a dataframe."""
    r_groups = [f"r{i}" for i in range(8)]
    df = pd.DataFrame(
        [[0] * 10],
        columns=["name", "r6"] + r_groups[:3] + ["r7", "step"] + r_groups[3:6],
    )
    assert find_r_groups(df) == r_groups


@mark.parametrize("energy", ["e_energy", "gibbs_energy"])
def test_enumeration_factory(energy: str) -> None:
    """Test creating an Enumeration from a csv file."""
    enm = enumeration_factory("tests/data/enum_2_3.csv", energy=energy)
    assert isinstance(enm, Enumeration)
    assert enm.paths.shape == (2, 3)
    assert len(enm.path_names) == 2


def test_enumeration_factory2() -> None:
    """Test creating an Enumeration from a csv file with multiple paths."""
    enm = enumeration_factory("tests/data/enum_2_2_2.csv")
    print(enm)
    assert isinstance(enm, Enumeration)
    assert enm.paths.shape == (2, 2, 2)
    assert len(enm.path_names) == 3
