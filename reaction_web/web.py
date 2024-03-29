from dataclasses import dataclass
from typing import Iterator, Sequence

from .path import Path


@dataclass
class Web:
    """
    A collection of reaction paths
    """

    paths: Sequence[Path]
    name: str = ""

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
        return f"<Web \"{self.name}\" [{', '.join(path.name for path in self)}]>"

    def __str__(self) -> str:
        return f"# {self.name}\n" + "\n\n".join(f"{path.name}:\n{path}" for path in self)

    def __getitem__(self, idx: int) -> Path:
        return self.paths[idx]

    def min(self) -> tuple[tuple[int, int], float]:
        """
        Index and value of the minimum achieved on the web path
        """
        i, (j, val) = min(
            enumerate(path.min() for path in self),
            key=lambda x: x[1][1],
        )

        return (i, j), val

    def max(self) -> tuple[tuple[int, int], float]:
        """
        Index and value of the maximimum achieved on the web path
        """
        i, (j, val) = max(
            enumerate(path.max() for path in self),
            key=lambda x: x[1][1],
        )

        return (i, j), val
