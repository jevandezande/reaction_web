"""Tests for the Path class."""

from pytest import approx, fixture, raises

from reaction_web import EReaction, Molecule, Path, Reaction


@fixture
def path1() -> Path:
    """Make a Path object of a -> b -> c -> d + e -> f – e⁻."""
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

    return Path([r1, r2, r3, r4], "1")


@fixture
def path2() -> Path:
    """Identical to path1 but without the first reaction, and with different step sizes."""
    refp = 5

    b = Molecule("b", 0)
    c = Molecule("c", 2)
    d = Molecule("d", -1)
    e = Molecule("e", 3)
    f = Molecule("f", 0.5)

    r2 = Reaction([b], [c])
    r3 = Reaction([c], [d, e])
    r4 = EReaction([e], [f], ne=1, ref_pot=refp)

    return Path([r2, r3, r4], "2", step_sizes=[2, -1, 3])


def test_len(path1: Path, path2: Path) -> None:
    """Test the __len__ method."""
    assert len(path1) == 4
    assert len(path2) == 3


def test_repr(path1: Path, path2: Path) -> None:
    """Test the __repr__ method."""
    assert repr(path1) == "<Path 1>"
    assert repr(path2) == "<Path 2>"


def test_str(path1: Path, path2: Path) -> None:
    """Test the __str__ method."""
    assert (
        str(path1)
        == """\
a -> b
b -> c
c -> d + e
e -> f + !5.00!"""
    )
    assert (
        str(path2)
        == """\
b -> c
c -> d + e
e -> f + !5.00!"""
    )


def test_getitem(path1: Path, path2: Path) -> None:
    """Test the __getitem__ method."""
    assert path1[1] == path1.reactions[1]
    assert path2[2] == path2.reactions[2]

    with raises(IndexError):
        path2[3]


def test_energies(path1: Path, path2: Path) -> None:
    """Test the energies property."""
    assert path1.energies == approx([-1, 2, 0, -7.5])
    assert path2.energies == approx([2, 0, -7.5])


def test_minmax(path1: Path, path2: Path) -> None:
    """Test the min and max methods."""
    assert path1.min() == (4, -6.5)
    assert path2.min() == (3, -5.5)
    assert path1.max() == (2, 1)
    assert path2.max() == (1, 2)
