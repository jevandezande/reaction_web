import numpy as np

from molecule import Molecule
from reaction import EReaction, Reaction

import matplotlib.pyplot as plt


class Path:
    def __init__(self, reactions, name=''):
        """
        Series of reactions forming a reaction path
        :param reactions: list of reactions in order
        """
        self.reactions = reactions
        self.name = name

    def __len__(self):
        return len(self.reactions)

    def __iter__(self):
        for reaction in self.reactions:
            yield reaction

    @property
    def energies(self):
        return np.array(list(map(lambda r: r.energy, self)))

    def plot(self, ax=plt):
        """
        Plot of the reaction path
        """
        xs, ys = [-0.5, 0.5], [0, 0]
        energy = 0
        for i, reaction in enumerate(self):
            energy += reaction.energy
            xs += [i + 0.6, i + 1.4]
            ys += [energy, energy]

        ax.plot(xs, ys, label=self.name)

        if ax == plt:
            plt.xticks(np.arange(len(self) + 1))
            plt.xlabel('Species')
            plt.title('Oxygen Evolution Free Energy Diagram')
