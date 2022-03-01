from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

from .chem_translate import translate
from .reaction import Reaction


@dataclass
class Path:
    """
    Series of reactions forming a reaction path
    """

    reactions: Sequence[Reaction]
    name: str = ""
    step_sizes: Optional[Iterable[float]] = None
    steps: np.ndarray = field(init=False)

    def __post_init__(self):
        step_sizes = self.step_sizes
        self.steps = np.zeros(len(self)) if step_sizes is None else np.array(step_sizes) - 1
        assert len(self.steps) == len(self.reactions)

    def __len__(self):
        """
        Number of reactions
        """
        return len(self.reactions)

    def __repr__(self):
        return f"<Path {self.name}>"

    def __str__(self):
        """
        String of the reactions
        """
        return "\n".join(f"{reaction}" for reaction in self)

    def __iter__(self) -> Iterator[Reaction]:
        """
        Iterate over reactions
        """
        yield from self.reactions

    @property
    def energies(self) -> np.ndarray:
        """
        An array of the energies of the reactions
        """
        return np.fromiter(map(lambda r: r.energy, self), dtype=float)

    def plot(self, plot: Optional[tuple] = None, spread: float | bool = True, latexify: bool = True) -> tuple:
        """
        Plot of the reaction path
        :param ax: where to plot
            e.g. using default canvas (plt) or a subplot (the given axis)
        """
        if plot is None:
            fig, ax = plt.subplots()
            ax.set_ylabel("Energy")
            ax.set_xticks(np.arange(len(self) + 1))
            ax.set_xlabel("Species")
        else:
            fig, ax = plot

        spread_width = 0.1 if spread is True else float(spread)

        length = len(self) + 1

        xs = np.repeat(np.arange(length), 2) + [-0.5 + spread_width, 0.5 - spread_width] * length
        xs[2:] += np.repeat(np.cumsum(self.steps), 2)

        # swap if going backwards
        for i in np.where(self.steps < 0)[0] * 2 + 2:
            xs[[i + 1, i]] = xs[[i, i + 1]]

        ys = np.append([0, 0], np.repeat(np.cumsum(self.energies), 2))

        label = translate(self.name) if latexify else self.name
        ax.plot(xs, ys, label=label)

        return fig, ax
