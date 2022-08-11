from pytest import fixture

from reaction_web import EReaction, Molecule, Path, Reaction, Web


@fixture
def web():
    refp = 5
    a = Molecule("a", 1)
    b = Molecule("b", 0)
    c = Molecule("c", 2)
    d = Molecule("d", -1)
    e = Molecule("e", 3)
    f = Molecule("f", 0.5)
    r1 = Reaction([a], [b])
    r2 = Reaction([b], [c])
    r3 = Reaction([c], [d, e])
    r4 = EReaction([e], [f], ne=1, ref_pot=refp)
    path1 = Path([r1, r2, r3, r4], "P1")
    path2 = Path([r2, r3, r4], "P2")
    path3 = Path([r2, r3, r4], "", step_sizes=[2, -1, 3])

    return Web([path1, path2, path3])


def test_iter(web):
    for path, p_original in zip(web, web.paths):
        assert path == p_original


def test_len(web):
    assert len(web) == 3


def test_repr(web):
    assert repr(web) == "<Web [P1, P2, ]>"


def test_str(web):
    assert (
        str(web)
        == """\
P1:
a -> b
b -> c
c -> d + e
e -> f + !5.00!

P2:
b -> c
c -> d + e
e -> f + !5.00!

:
b -> c
c -> d + e
e -> f + !5.00!"""
    )
