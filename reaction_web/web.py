"""A collection of reaction Paths."""

from dataclasses import dataclass
from typing import Iterator, Sequence

from .path import Path


@dataclass
class Web:
    """A collection of reaction Paths."""

    paths: Sequence[Path]
    name: str = ""

    def __iter__(self) -> Iterator[Path]:
        """Iterate over all reaction Paths."""
        yield from self.paths

    def __len__(self) -> int:
        """Count of Paths in the Web."""
        return len(self.paths)

    def __repr__(self) -> str:
        """Representation of the Web."""
        return f"<Web \"{self.name}\" [{', '.join(path.name for path in self)}]>"

    def __str__(self) -> str:
        """Convert to a string."""
        return f"# {self.name}\n" + "\n\n".join(f"{path.name}:\n{path}" for path in self)

    def __getitem__(self, idx: int) -> Path:
        """
        Index into the Paths.

        :param idx: index of the Path
        :return: the Path at the index
        """
        return self.paths[idx]

    def min(self) -> tuple[tuple[int, int], float]:
        """Index and value of the minimum achieved on the web Path."""
        i, (j, val) = min(
            enumerate(path.min() for path in self),
            key=lambda x: x[1][1],
        )

        return (i, j), val

    def max(self) -> tuple[tuple[int, int], float]:
        """Index and value of the maximimum achieved on the web Path."""
        i, (j, val) = max(
            enumerate(path.max() for path in self),
            key=lambda x: x[1][1],
        )

        return (i, j), val
