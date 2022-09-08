from typing import Sequence

import more_itertools as mit
import pandas as pd

from .. import Molecule, Path, Reaction, Web


def read_r_group_dataframe(infile):
    """
    Assumes the data has been cleaned!!!
    """
    data = pd.read_csv(infile)
    assert "step" in data.columns
    assert "energy" in data.columns

    r_groups = find_r_groups(data)
    # data = data.sorted(r_groups + ["step"])

    return webify(data, r_groups)


def find_r_groups(data: pd.DataFrame):
    """
    Find all of the r-groups in a DataFrame
    """
    return [name for name in data.columns if name[0] == "r" and name[1:].isnumeric()]


def pathify(data: pd.DataFrame, path_name: str = "") -> Path:
    """
    Generates a path from sequential energy data.

    Assumes data is sorted and contains "name" and "energy" columns
    """
    molecules = [Molecule(name, energy) for name, energy in zip(data["name"], data["energy"])]

    reactions = [Reaction([reactant], [product]) for reactant, product in mit.windowed(molecules, 2)]

    return Path(reactions, path_name)


# WEB_DICT = dict[str, Web] | dict[str, "WEB_DICT"]


def webify(data: pd.DataFrame, r_groups: Sequence[str], name: str = ""):  # -> Web | WEB_DICT:
    if len(r_groups) < 1:
        raise ValueError(f"Expected ≥ 1 r-group, got: {r_groups=}")

    if len(r_groups) == 1:
        return Web([pathify(path_data, r_group) for r_group, path_data in data.groupby(r_groups)], name)

    head, *tail = r_groups
    return {r_group: webify(values, tail, r_group) for r_group, values in data.groupby(head)}
