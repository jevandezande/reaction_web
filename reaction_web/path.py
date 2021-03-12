import numpy as np

from .molecule import Molecule
from .reaction import EReaction, Reaction

import matplotlib.pyplot as plt


class Path:
    def __init__(self, reactions, name='', step_sizes = None):
        """
        Series of reactions forming a reaction path
        :param reactions: list of reactions in order
        :param name: name of the reaction path
        """
        self.reactions = reactions
        self.name = name
        self.steps = np.zeros(len(reactions)) if step_sizes is None else np.array(step_sizes) - 1
        assert len(self.steps) == len(reactions)

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
        yield from self.reactions

    @property
    def energies(self):
        """
        An array of the energies of the reactions
        """
        return np.fromiter(map(lambda r: r.energy, self), dtype=float)

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

        length = len(self) + 1

        xs = np.repeat(np.arange(length), 2) + [-0.5 + spread_width, 0.5 - spread_width]*length
        xs[2:] += np.repeat(np.cumsum(self.steps), 2)

        # swap if going backwards
        for i in np.where(self.steps < 0)[0]*2 + 2:
            xs[[i+1, i]] = xs[[i, i + 1]]

        ys = np.append([0, 0], np.repeat(np.cumsum(self.energies), 2))

        ax.plot(xs, ys, label=self.name)

        return fig, ax
