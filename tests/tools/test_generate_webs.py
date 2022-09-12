import pandas as pd
from pytest import fixture

from reaction_web.tools.generate_webs import find_r_groups, pathify, read_r_group_dataframe, webify


@fixture
def data():
    return pd.read_csv("tests/tools/r_group_data.csv")


def test_find_r_groups(data):
    assert find_r_groups(data) == ["r1", "r2", "r3"]


def test_pathify(data):
    data_H = data[(data["r1"] == "H") & (data["r2"] == "H") & (data["r3"] == "B")]
    data_C = data[(data["r1"] == "C") & (data["r2"] == "H") & (data["r3"] == "B")]

    path_H = pathify(data_H, "H")
    path_C = pathify(data_C, "C")

    assert len(path_H) == 2
    assert len(path_C) == 2

    assert path_H.name == "H"
    assert path_C.name == "C"

    assert all(path_H.energies == [1, 1])
    assert all(path_C.energies == [2, 2])


def test_webify(data):
    data_r1_H_B = data[(data["r2"] == "H") & (data["r3"] == "B")]
    web_r1_H_B = webify(data_r1_H_B, ["r1"])
    assert len(web_r1_H_B) == 3

    data_r1_r2_B = data[data["r3"] == "B"]
    webs_r1_r2_B = webify(data_r1_r2_B, ["r1", "r2"])
    assert len(webs_r1_r2_B) == 3
    assert tuple(webs_r1_r2_B.keys()) == ("C", "CC", "H")
    for web in webs_r1_r2_B.values():
        assert len(web) == 2

    webs = webify(data, ["r1", "r2", "r3"])
    assert len(webs) == 3
    for r1, web_group in webs.items():
        assert len(web_group) == 2
        for r2, web in web_group.items():
            assert web.name == f"{r1} {r2}"
            assert len(web) == 2 if r2 == "B" else 1

    path_B, path_Si = webs["C"]["Cl"]
    assert path_B.name == "C Cl B"
    assert path_Si.name == "C Cl Si"
    assert all(path_B.energies == path_Si.energies)


def test_r_group_dataframe(data):
    webs = read_r_group_dataframe("tests/tools/r_group_data.csv")
    assert len(webs) == 3
    for r1, web_group in webs.items():
        assert len(web_group) == 2
        for r2, web in web_group.items():
            assert web.name == f"{r1} {r2}"
            assert len(web) == 2 if r2 == "B" else 1
