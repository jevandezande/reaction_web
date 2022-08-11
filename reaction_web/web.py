from dataclasses import dataclass
from typing import Iterator, Sequence

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
