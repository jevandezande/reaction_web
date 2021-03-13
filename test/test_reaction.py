from pytest import raises

from reaction_web import EReaction, Molecule, Reaction


def test_Reaction():
    a = Molecule("a", -1)
    b = Molecule("b", -2)
    r = Reaction([a], [b])

    assert r.reactants == [a]
    assert r.products == [b]
    assert r.energy == -1
    assert str(r) == "a -> b"

    with raises(AssertionError):
        assert Reaction(a, b)


def test_EReaction():
    a = Molecule("a", -1)
    b = Molecule("b", -2)
    r = EReaction([a], [b], ne=1, ref_pot=1)

    assert r.reactants == [a]
    assert r.products == [b]
    assert r.energy == -2
    assert str(r) == "a -> b + !1.00!"

    with raises(AssertionError):
        assert EReaction(a, b, 9.0, -4.4)
