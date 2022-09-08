import pandas as pd
from pytest import fixture

from reaction_web.tools.generate_webs import find_r_groups, pathify


@fixture
def data():
    return pd.read_csv("tests/tools/r_group_data.csv")


def test_find_r_groups(data):
    assert find_r_groups(data) == ["r1", "r2"]


def test_pathify(data):
    data_H = data[(data["r1"] == "H") & (data["r2"] == "H")]
    data_C = data[(data["r1"] == "C") & (data["r2"] == "H")]

    path_H = pathify(data_H, "H")
    path_C = pathify(data_C, "C")

    assert len(path_H) == 2
    assert len(path_C) == 2

    assert path_H.name == "H"
    assert path_C.name == "C"

    assert all(path_H.energies == [1, 1])
    assert all(path_C.energies == [2, 2])
