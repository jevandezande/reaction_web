from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np

from .path import Path


@dataclass
class Enumeration:
    """
    A collection of reaction paths that all have the same form

    :param path_names:
        {"r1": ("H", "C"), "r2": ("H", "B", "I")}
    """

    paths: np.ndarray
    path_names: dict[str, tuple[str, ...]]

    def __post_init__(self):
        path_names_shape = tuple(map(len, self.path_names.values()))
        if path_names_shape != self.paths.shape:
            raise ValueError(
                "Expected paths and path_names to have the same shape, got {paths.shape=} != {paths_names_shape=}"
            )

    def __repr__(self) -> str:
        return f"<Enumeration {tuple(self.path_names)} {self.shape}>"

    def __str__(self) -> str:
        """
        Recursively generate a representation of the Enumeration
        """
        out = f"Enumeration {self.path_names}\n"
        if self.ndim == 1:  # 1-dimensional array of Paths
            return out + "\n".join(map(repr, self))

        path_name, subs = next(iter(self.path_names.items()))

        for enm, sub in zip(self, subs):
            # assert isinstance(enm, Enumeration)
            enm_str = str(enm).replace("\n", "\n    ").replace("\n    \n", "\n\n")
            out += f"\n{path_name}: {sub}\n{enm_str}\n"
        return out.strip()

        # TODO: Add TypeGuards

    #         return f"Enumeration {self.path_names}\n" + "\n".join(
    #             f"""
    # {path_name}: {sub}
    # Enumeration {enm.path_names}
    # {enm}"""
    #             for enm, sub in zip(self, subs)
    #         )

    def __len__(self) -> int:
        """
        Length of the 0-th dimension of the Enumeration
        """
        return len(self.paths)

    def __getitem__(self, idx: str | int) -> Enumeration | Path:
        """
        Get an Enumeration/Path via its path_name (str) or index (int)
        """
        (path_name, subs), *tail = self.path_names.items()
        if isinstance(idx, str):
            if idx not in subs:
                raise KeyError("{idx=} is not contained in Enumeration")
            idx = subs.index(idx)

        item = self.paths[idx]

        return Enumeration(item, dict(tail)) if tail else item

    def __iter__(self) -> Iterator[Enumeration | Path]:
        if self.ndim == 1:
            yield from self.paths  # Iterator[Path]
        else:
            head, *tail = self.path_names.items()
            yield from (Enumeration(item, dict(tail)) for item in self.paths)  # Iterator[Enumeration]

    @property
    def shape(self) -> tuple[int, ...]:
        return self.paths.shape

    @property
    def ndim(self) -> int:
        return self.paths.ndim
