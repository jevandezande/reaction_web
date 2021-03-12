from __future__ import annotations

from typing import Generator, Literal, Sequence

import matplotlib.pyplot as plt
import more_itertools as mit
import numpy as np

from .path import Path


class Web:
    def __init__(self, paths: Sequence[Path]):
        """
        A collection of reaction paths
        :param paths: Paths
        """
        self.paths = paths

    def __iter__(self) -> Generator[Path, None, None]:
        """
        Iterate over all reaction paths
        """
        yield from self.paths

    def __len__(self):
        """
        Number of paths in the Web
        """
        return len(self.paths)

    def __repr__(self):
        paths = ", ".join(path.name for path in self)
        return f"<Web [{paths}]>"

    def __str__(self):
        return "\n\n".join(f"{path.name}:\n{path}" for path in self)

    def plot(self, style: Literal["stacked", "subplots"] = "stacked", spread: float | bool = True):
        """
        Plot the reaction paths.

        :param style: style of plots:
            stacked: all paths on the same plot
            subplots: each path in its own subplot
        """
        if style == "stacked":
            fig, axes = plt.subplots()
            axes_flat = [axes] * len(self)

        elif style == "subplots":
            height = int(np.sqrt(len(self.paths)))
            width = height + 1 if height ** 2 < len(self.paths) else height

            fig, axes = plt.subplots(height, width, sharex=True, sharey=True)
            fig.subplots_adjust(hspace=0, wspace=0)
            axes_flat = list(mit.collapse(axes))

        max_len = max([len(path) for path in self])
        axes_flat[0].set_xticks(np.arange(max_len + 1))
        axes_flat[0].set_ylabel("Energy")

        max_len = 0
        for path, ax in zip(self, axes_flat):
            path.plot(plot=(fig, ax), spread=spread)
            ax.legend()
            ax.set_xlabel("Species")

        return fig, axes
