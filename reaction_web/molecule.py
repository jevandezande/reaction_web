"""Molecule class representing an item with an energy."""

from dataclasses import dataclass


@dataclass
class Molecule:
    """A molecule, atom, or group of these that have a defined energy."""

    name: str
    energy: float

    def __repr__(self) -> str:
        """
        Representation of the Molecule.

        >>> Molecule("H₂O", -1.0)
        <Mol H₂O -1.0000>
        """
        return f"<Mol {self.name} {self.energy:7.4f}>"
