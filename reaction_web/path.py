import numpy as np

from .molecule import Molecule
from .reaction import EReaction, Reaction

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

    def __repr__(self):
        reactions = ''
        return f'<Path {self.name}>'

    def __str__(self):
        """
        String of the reactions
        """
        return '\n'.join(f'{reaction}' for reaction in self)

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

    def plot(self, plot=None, spread=True):
        """
        Plot of the reaction path
        :param ax: where to plot
            e.g. using default canvas (plt) or a subplot (the given axis)
        """
        if plot is None:
            fig, ax = plt.subplots()
            ax.set_ylabel('Energy')
            ax.set_xticks(np.arange(len(self) + 1))
            ax.set_xlabel('Species')
        else:
            fig, ax = plot

        if not spread:
            spread_width = 0
        elif spread is True:
            spread_width = 0.1
        else:
            spread_width = spread

        xs, ys = [-0.5 + spread_width, 0.5 - spread_width], [0, 0]

        for i, energy in enumerate(np.cumsum(self.energies)):
            xs += [i + 0.5 + spread_width, i + 1.5 - spread_width]
            ys += [energy, energy]

        ax.plot(xs, ys, label=self.name)

        return fig, ax
