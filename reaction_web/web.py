from dataclasses import dataclass
from typing import Generator, Literal, Optional, Sequence

import matplotlib.pyplot as plt
import more_itertools as mit
import numpy as np

from .path import Path


@dataclass
class Web:
    """
    A collection of reaction paths
    """

    paths: Sequence[Path]

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
        return f"<Web [{', '.join(path.name for path in self)}]>"

    def __str__(self):
        return "\n\n".join(f"{path.name}:\n{path}" for path in self)

    def plot(
        self,
        title: Optional[str] = None,
        style: Literal["stacked", "subplots"] = "stacked",
        spread: float | bool = True,
        latexify: bool = True,
    ):
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
            height = int(np.sqrt(len(self)))
            width = -(len(self) // -height)  # Ceiling integer division

            fig, axes = plt.subplots(height, width, sharex=True, sharey=True)
            fig.subplots_adjust(hspace=0, wspace=0)
            axes_flat = list(mit.collapse(axes))

        max_len = max(len(path) for path in self)
        axes_flat[0].set_xticks(np.arange(max_len + 1))
        axes_flat[0].set_ylabel("Energy")

        for path, ax in zip(self, axes_flat):
            path.plot(plot=(fig, ax), spread=spread, latexify=latexify)
            ax.legend()
            ax.set_xlabel("Species")

        fig.suptitle(title)

        return fig, axes
