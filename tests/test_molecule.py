from reaction_web import Molecule


def test_init():
    a = Molecule("a", -1)
    assert a.name == "a"
    assert a.energy == -1
    assert str(a) == "<Mol a -1.0000>"
    assert repr(a) == "<Mol a -1.0000>"
