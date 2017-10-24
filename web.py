import numpy as np

from path import Path
from molecule import Molecule
from reaction import EReaction, Reaction

import more_itertools as mit
import matplotlib.pyplot as plt


class Web:
    def __init__(self, paths):
        self.paths = paths

    def __iter__(self):
        for path in self.paths:
            yield path

    def plot(self, name=None, style='stacked'):
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


if __name__ == "__main__":
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
    r4 = EReaction([e], [f], ref_pot=refp)
    path1 = Path([r1, r2, r3, r4])
    path2 = Path([r2, r3, r4])

    web = Web([path1, path2])
    web.plot(style='subplots')
    plt.show()
    web.plot(style='stacked')
    plt.show()
