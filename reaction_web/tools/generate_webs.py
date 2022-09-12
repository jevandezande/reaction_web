from typing import Sequence

import more_itertools as mit
import pandas as pd

from .. import Molecule, Path, Reaction, Web

# Recursive types are not yet available in mypy: https://github.com/python/mypy/pull/13297
# WEB_DICT = dict[str, Web] | dict[str, "WEB_DICT"]


def read_r_group_dataframe(infile: str):  # -> WEB_DICT:
    """
    Reads a DataFrame and generates Paths based on r-groups.

    :param infile: csv file to read
    :return: recursive dictionary of Webs
    """
    data = pd.read_csv(infile)
    assert "step" in data.columns
    assert "energy" in data.columns

    r_groups = find_r_groups(data)

    return webify(data, r_groups)


def find_r_groups(data: pd.DataFrame) -> list[str]:
    """
    Finds all r-groups in a DataFrame (all columns of form "r#").

    :param data: DataFrame in which to find the r-groups
    :return: names of all r-groups
    """
    return [name for name in data.columns if name[0] == "r" and name[1:].isnumeric()]


def pathify(data: pd.DataFrame, path_name: str = "") -> Path:
    """
    Generates a Path from energy data. Each row is a Molecule, and adjacent
    rows are Reactions.

    Assumes data is sorted and contains "name" and "energy" columns.

    :param data: DataFrame in which to find the r-groups
    :param path_name: name for the Path
    :return: Path with each step in the Reaction
    """
    molecules = [Molecule(name, energy) for name, energy in zip(data["name"], data["energy"])]

    reactions = [Reaction([reactant], [product]) for reactant, product in mit.windowed(molecules, 2)]

    return Path(reactions, path_name)


def webify(data: pd.DataFrame, r_groups: Sequence[str], name: str = ""):  # -> Web | WEB_DICT:
    """
    Generates Webs from a DataFrame. Each successive level of the output
    dictionary is an r-group, with the lowest Web containing Paths for each
    manifestation of the final r-group.

    Assumes the steps are sorted and ignores step labels.

    :param data: data used to generate Webs
    :param r_groups: r-groups labels to be used for generating Paths
    :param name: name for the Web (also pre-pended on its children)
    :return: recursive dictionary of Webs
    """
    if len(r_groups) < 1:
        raise ValueError(f"Expected ≥ 1 r-group, got: {r_groups=}")

    if len(r_groups) == 1:
        return Web([pathify(path_data, f"{name} {r}") for r, path_data in data.groupby(r_groups)], name)

    head, *tail = r_groups
    return {r: webify(values, tail, f"{name} {r}".strip()) for r, values in data.groupby(head)}
