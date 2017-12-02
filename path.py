import numpy as np

from molecule import Molecule
from reaction import EReaction, Reaction

import matplotlib.pyplot as plt


class Path:
    def __init__(self, reactions, name=''):
        """
        Series of reactions forming a reaction path
        :param reactions: list of reactions in order
        :param name: name of the reaction path
        """
        self.reactions = reactions
        self.name = name

    def __len__(self):
        """
        Number of reactions
        """
        return len(self.reactions)

    def __iter__(self):
        """
        Iterate over reactions
        """
        for reaction in self.reactions:
            yield reaction

    @property
    def energies(self):
        """
        An array of the energies of the reactions
        """
        return np.array(list(map(lambda r: r.energy, self)))

    def plot(self, ax=plt):
        """
        Plot of the reaction path
        :param ax: where to plot
            e.g. using default canvas (plt) or a subplot (the given axis)
        """
        xs, ys = [-0.4, 0.4], [0, 0]

        for i, energy in enumerate(np.cumsum(self.energies)):
            xs += [i + 0.6, i + 1.4]
            ys += [energy, energy]

        ax.plot(xs, ys, label=self.name)

        if ax == plt:
            plt.xticks(np.arange(len(self) + 1))
            plt.xlabel('Species')
