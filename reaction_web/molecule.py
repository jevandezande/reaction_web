from dataclasses import dataclass


@dataclass
class Molecule:
    """
    A molecule, atom, or group of these that have a defined energy
    """

    name: str
    energy: float

    def __repr__(self) -> str:
        return f"<Mol {self.name} {self.energy:7.4f}>"
