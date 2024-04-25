"""Tests for the Web class."""

from pytest import fixture, raises

from reaction_web import EReaction, Molecule, Path, Reaction, Web


@fixture
def web() -> Web:
    """Make a simple Web with three paths."""
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

    return Web([path1, path2, path3], "My Web")


def test_iter(web: Web) -> None:
    """Test that the Web is iterable."""
    for path, p_original in zip(web, web.paths):
        assert path == p_original


def test_len(web: Web) -> None:
    """Test that the Web has the correct length."""
    assert len(web) == 3


def test_repr(web: Web) -> None:
    """Test the repr of the Web."""
    assert repr(web) == '<Web "My Web" [P1, P2, ]>'


def test_str(web: Web) -> None:
    """Test the str of the Web."""
    assert (
        str(web)
        == """\
# My Web
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


def test_getitem(web: Web) -> None:
    """Test getting items from the Web."""
    path0, path1, path2 = web
    assert web[0] == path0
    assert web[1] == path1
    assert web[2] == path2

    with raises(IndexError):
        web[3]


def test_minmax(web: Web) -> None:
    """Test the min and max of the Web."""
    assert web.min() == ((0, 4), -6.5)
    assert web.max() == ((1, 1), 2)
