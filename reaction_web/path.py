"""Path class for a series of Reactions forming a Path."""

from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence

import numpy as np

from .reaction import Reaction


@dataclass
class Path:
    """Series of Reactions forming a Path."""

    reactions: Sequence[Reaction]
    name: str = ""
    step_sizes: Iterable[float] | None = None
    steps: np.ndarray = field(init=False)

    def __post_init__(self):
        """Ensure that the step_sizes and Reactions have the same length."""
        step_sizes = self.step_sizes
        self.steps = np.zeros(len(self)) if step_sizes is None else np.array(step_sizes) - 1
        assert len(self.steps) == len(self.reactions)

    def __len__(self) -> int:
        """Count of Reactions in Path."""
        return len(self.reactions)

    def __repr__(self) -> str:
        """Representation of the Path."""
        return f"<Path {self.name}>"

    def __str__(self) -> str:
        """Convert to a string."""
        return "\n".join(f"{reaction}" for reaction in self)

    def __iter__(self) -> Iterator[Reaction]:
        """Iterate over the Reactions."""
        yield from self.reactions

    def __getitem__(self, idx: int) -> Reaction:
        """
        Index into the Reactions.

        :param idx: index of the Reaction
        :return: the Reaction at the index
        """
        return self.reactions[idx]

    def min(self) -> tuple[int, float]:
        """Index and value of the minimum achieved along the Path."""
        return min(enumerate(self.relative_energies), key=lambda x: x[1])

    def max(self) -> tuple[int, float]:
        """Index and value of the maximum achieved along the Path."""
        return max(enumerate(self.relative_energies), key=lambda x: x[1])

    @property
    def energies(self) -> np.ndarray:
        """An array of the energies of the Reactions."""
        return np.fromiter(map(lambda r: r.energy, self), dtype=float)

    @property
    def relative_energies(self) -> np.ndarray:
        """An array of the cumulative energy along the Path."""
        return np.cumsum([0.0] + [r.energy for r in self])
