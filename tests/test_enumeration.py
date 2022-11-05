from itertools import product

import more_itertools as mit
from pytest import fixture, raises

from reaction_web import Enumeration, Path
from reaction_web.tools.generate_paths import enumeration_factory


@fixture(params=["e_energy", "gibbs_energy"])
def data_enumeration(request):
    return enumeration_factory("tests/data/enum_2_3.csv", energy=request.param)


@fixture
def data_2_2_2_enumeration():
    return enumeration_factory("tests/data/enum_2_2_2.csv")


def test_Enumeration_repr(data_enumeration):
    assert repr(data_enumeration) == "<Enumeration ('r1', 'r2') (2, 3)>"


def test_Enumeration_str(data_enumeration):
    assert (
        str(data_enumeration)
        == """\
Enumeration {'r1': ('C', 'H'), 'r2': ('B', 'H', 'I')}

r1: C
Enumeration {'r2': ('B', 'H', 'I')}
    <Path ('C', 'B')>
    <Path ('C', 'H')>
    <Path ('C', 'I')>

r1: H
Enumeration {'r2': ('B', 'H', 'I')}
    <Path ('H', 'B')>
    <Path ('H', 'H')>
    <Path ('H', 'I')>"""
    )


def test_Enumeration_str_2(data_2_2_2_enumeration):
    assert (
        str(data_2_2_2_enumeration)
        == """\
Enumeration {'r1': ('B', 'H'), 'r2': ('C', 'H'), 'r3': ('H', 'I')}

r1: B
Enumeration {'r2': ('C', 'H'), 'r3': ('H', 'I')}

    r2: C
    Enumeration {'r3': ('H', 'I')}
        <Path ('B', 'C', 'H')>
        <Path ('B', 'C', 'I')>

    r2: H
    Enumeration {'r3': ('H', 'I')}
        <Path ('B', 'H', 'H')>
        <Path ('B', 'H', 'I')>

r1: H
Enumeration {'r2': ('C', 'H'), 'r3': ('H', 'I')}

    r2: C
    Enumeration {'r3': ('H', 'I')}
        <Path ('H', 'C', 'H')>
        <Path ('H', 'C', 'I')>

    r2: H
    Enumeration {'r3': ('H', 'I')}
        <Path ('H', 'H', 'H')>
        <Path ('H', 'H', 'I')>"""
    )


def test_Enumeration_len(data_enumeration):
    assert len(data_enumeration) == 2


def test_Enumeration_getitem(data_enumeration):
    assert isinstance(data_enumeration["H"], Enumeration)
    assert isinstance(data_enumeration["C"], Enumeration)
    for a, b in product("HC", "HBI"):
        path = data_enumeration[a][b]
        assert isinstance(path, Path)
        assert len(path) == 3
        assert path.name == str((a, b))

    with raises(KeyError):
        assert data_enumeration["B"]


def test_Enumeration_iter(data_enumeration):
    for enum_r1 in data_enumeration:
        for path in enum_r1:
            for (reactants, products), (name_r, name_p) in zip(path, mit.windowed("ABCD", 2)):
                assert reactants[0].name == name_r
                assert products[0].name == name_p


def test_Enumeration_iter_2(data_2_2_2_enumeration):
    for enum_r1 in data_2_2_2_enumeration:
        for enum_r2 in enum_r1:
            for path in enum_r2:
                (reaction,) = path
                for (molecule,), name in zip(reaction, "AB"):
                    assert molecule.name == name


def test_Enumeration_shape(data_enumeration):
    assert data_enumeration.shape == (2, 3)
