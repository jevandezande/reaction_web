from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence

import numpy as np

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

    def __len__(self) -> int:
        """
        Number of reactions
        """
        return len(self.reactions)

    def __repr__(self) -> str:
        return f"<Path {self.name}>"

    def __str__(self) -> str:
        """
        String of the reactions
        """
        return "\n".join(f"{reaction}" for reaction in self)

    def __iter__(self) -> Iterator[Reaction]:
        """
        Iterate over reactions
        """
        yield from self.reactions

    def __getitem__(self, idx: int) -> Reaction:
        """
        Index into the reactions
        """
        return self.reactions[idx]

    def min(self) -> tuple[int, float]:
        """
        Index and value of the minimum achieved along path
        """
        return min(enumerate(self.relative_energies), key=lambda x: x[1])

    def max(self) -> tuple[int, float]:
        """
        Index and value of the maximum achieved along path
        """
        return max(enumerate(self.relative_energies), key=lambda x: x[1])

    @property
    def energies(self) -> np.ndarray:
        """
        An array of the energies of the reactions
        """
        return np.fromiter(map(lambda r: r.energy, self), dtype=float)

    @property
    def relative_energies(self) -> np.ndarray:
        """
        An array of the cumulative energy along the path
        """
        return np.cumsum([0.0] + [r.energy for r in self])
