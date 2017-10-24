#!/usr/bin/env python3
import os

from path import Path
from molecule import Molecule
from reaction import EReaction, Reaction

import pytest

from pytest import approx


class TestMolecule:
    def test(self):
        a = Molecule('a', -1)
        assert a.name == 'a'
        assert a.energy == -1
        assert str(a) == '<a -1.0000>'


class TestReaction:
    def test(self):
        a = Molecule('a', -1)
        b = Molecule('b', -2)
        r = Reaction([a], [b])

        assert r.reactants == [a]
        assert r.products == [b]
        assert r.energy == -1
        assert str(r) == 'a -> b'

        with pytest.raises(AssertionError):
            assert Reaction(a, b)


class TestEReaction(TestReaction):
    def test(self):
        a = Molecule('a', -1)
        b = Molecule('b', -2)
        r = EReaction([a], [b], ne=1, ref_pot=1)

        assert r.reactants == [a]
        assert r.products == [b]
        assert r.energy == -2
        assert str(r) == 'a -> b + !1.00!'

        with pytest.raises(AssertionError):
            assert Reaction(a, b)


class TestPath:
    def test(self):
        refp = 5
        a = Molecule('a', 1)
        b = Molecule('b', 0)
        c = Molecule('c', 2)
        d = Molecule('d', -1)
        e = Molecule('e', 3)
        f = Molecule('f', 0.5)
        r1 = Reaction([a], [b])
        r2 = Reaction([b], [c])
        r3 = Reaction([c], [d, e])
        r4 = EReaction([e], [f], ne=1, ref_pot=refp)
        path1 = Path([r1, r2, r3, r4])
        path2 = Path([r2, r3, r4])

        assert path1.reactions == [r1, r2, r3, r4]
        assert path2.reactions == [r2, r3, r4]

        assert path1.energies == approx([-1, 2, 0, -7.5])
        assert path2.energies == approx([2, 0, -7.5])
