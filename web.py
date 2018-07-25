import numpy as np

from .path import Path
from .molecule import Molecule
from .reaction import EReaction, Reaction

import more_itertools as mit
import matplotlib.pyplot as plt


class Web:
    def __init__(self, paths):
        """
        A collection of reaction paths
        :param paths: a list of paths
        """
        assert isinstance(paths, list)
        self.paths = paths

    def __iter__(self):
        """
        Iterate over all reaction paths
        """
        for path in self.paths:
            yield path

    def __repr__(self):
        paths = ", ".join(path.name for path in self)
        return f'<Web [{paths}]>'

    def __str__(self):
        return '\n\n'.join(f'{path.name}:\n{path}' for path in self)

    def plot(self, style='stacked'):
        """
        Plot the reaction paths
        :param style: style of plots:
            stacked: all paths on the same plot
            subplots: each path in its own subplot
        """
        if style == 'stacked':
            for path in self:
                path.plot()
        elif style == 'subplots':
            height = int(np.sqrt(len(self.paths)))
            width = height + 1 if height**2 < len(self.paths) else height

            f, axes = plt.subplots(height, width, sharex=True, sharey=True)
            axes_iter = mit.collapse(axes)
            max_len = 0
            for i, (path, ax) in enumerate(zip(self, axes_iter)):
                path.plot(ax=ax)
                max_len = max(max_len, len(path))
            plt.xticks(np.arange(max_len + 1))
            plt.xlabel('Species')
