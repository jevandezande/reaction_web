from dataclasses import dataclass
from typing import Optional


@dataclass
class Molecule:
    """
    A molecule, atom, or group of these that have a defined energy
    """

    name: str
    energy: float
    multiplicity: Optional[int] = None

    def __repr__(self):
        return f"<{self.name} {self.energy:7.4f}>"
