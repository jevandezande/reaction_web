from pytest import approx

from reaction_web import EReaction, Molecule, Path, Reaction


def test_Path():
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
    path1 = Path([r1, r2, r3, r4])
    path2 = Path([r2, r3, r4], step_sizes=[2, -1, 3])

    assert path1.reactions == [r1, r2, r3, r4]
    assert path2.reactions == [r2, r3, r4]

    assert path1.energies == approx([-1, 2, 0, -7.5])
    assert path2.energies == approx([2, 0, -7.5])
