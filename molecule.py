class Molecule:
    def __init__(self, name, energy):
        """
        A molecule, atom, or group of these that have a defined energy
        """
        self.name = name
        self.energy = energy

    def __repr__(self):
        return f'<{self.name} {self.energy:7.4f}>'

    def __str__(self):
        return self.__repr__()
