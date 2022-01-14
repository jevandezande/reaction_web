from reaction_web import Molecule


def test_init():
    a = Molecule("a", -1)
    assert a.name == "a"
    assert a.energy == -1
    assert str(a) == "<a -1.0000>"
