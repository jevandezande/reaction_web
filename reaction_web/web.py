from dataclasses import dataclass
from typing import Iterator, Literal, Optional, Sequence

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

    def __iter__(self) -> Iterator[Path]:
        """
        Iterate over all reaction paths
        """
        yield from self.paths

    def __len__(self) -> int:
        """
        Number of paths in the Web
        """
        return len(self.paths)

    def __repr__(self) -> str:
        return f"<Web [{', '.join(path.name for path in self)}]>"

    def __str__(self) -> str:
        return "\n\n".join(f"{path.name}:\n{path}" for path in self)

    def plot(
        self,
        title: Optional[str] = None,
        style: Literal["stacked", "subplots"] = "stacked",
        plot: Optional[tuple] = None,
        spread: float | bool = True,
        xtickslabels: Optional[list[str]] = None,
        latexify: bool = True,
    ) -> tuple:
        """
        Plot the reaction paths.

        :param style: style of plots:
            stacked: all paths on the same plot
            subplots: each path in its own subplot
        :param plot: where to plot the Path
            e.g. using default canvas (plt) or a subplot (the given axis)
        :param spread: how much to spread the connecting lines
        :param xtickslabels: labels for the xticks (replaces numbers)
        :param latexify: convert names to latex
        """
        if not plot:
            if style == "stacked":
                fig, axes = plt.subplots()
                axes_flat = [axes] * len(self)

            elif style == "subplots":
                height = int(np.sqrt(len(self)))
                width = -(len(self) // -height)  # Ceiling integer division

                fig, axes = plt.subplots(height, width, sharex=True, sharey=True)
                fig.subplots_adjust(hspace=0, wspace=0)
                axes_flat = list(mit.collapse(axes))
        else:
            fig, axes = plot
            axes_flat = [axes] * len(self)

        max_len = max(len(path) for path in self)
        axes_flat[0].set_xticks(np.arange(max_len + 1))
        axes_flat[0].set_ylabel("Energy")

        for path, ax in zip(self, axes_flat):
            path.plot(plot=(fig, ax), spread=spread, latexify=latexify)
            ax.legend()
            ax.set_xlabel("Species")

        if xtickslabels:
            ax.set_xticklabels(xtickslabels)

        if title:
            if plot:
                plot[1].set_title(title)
            else:
                fig.suptitle(title)

        return fig, axes
