from itertools import product
from typing import Sequence

import more_itertools as mit
import numpy as np
import pandas as pd
from natsort import natsorted

from .. import Enumeration, Molecule, Path, Reaction


def enumeration_factory(
    infile: str,
    energy: str = "energy",
    name: str = "name",
    path_indicators: Sequence[str] | str = "r-groups",
    **csv_kwargs,
) -> Enumeration:
    paths_dict, pi_dict = read_multipath_csv(infile, energy=energy)

    shape = tuple(len(vals) for vals in pi_dict.values())
    paths = np.zeros(shape, dtype=object)
    for values, idxs in zip(
        product(*pi_dict.values()),
        product(*map(range, shape)),
    ):
        paths[idxs] = paths_dict[values]

    return Enumeration(paths, pi_dict)


def read_csv(infile: str, energy: str = "energy", name: str = "name", **csv_kwargs) -> list[Molecule]:
    """
    Read a csv with Molecule data

    :param infile: file to read
    :param energy: column to use for molecule energy
    :param name: column to use for molecule name
    :param csv_kwargs: parameters for csv parsing
    :return: Molecules generated from data
    """
    csv_kwargs = {"skipinitialspace": True} | csv_kwargs
    df = pd.read_csv(infile, **csv_kwargs)
    df = df.convert_dtypes(infer_objects=True)

    return [Molecule(data[name], data[energy]) for _, data in df.iterrows()]


def read_multipath_csv(
    infile: str,
    energy: str = "energy",
    name: str = "name",
    path_indicators: Sequence[str] | str = "r-groups",
    **csv_kwargs,
) -> tuple[dict[tuple[str, ...], Path], dict[str, tuple[str, ...]]]:
    """
    Read molecule data in a CSV and convert into paths

    Note:
        Only utilizes step data to sort, no combination yet available

    :param infile: file to read
    :param energy: column to use for molecule energy
    :param name: column to use for molecule name
    :param path_indicators: columns that indicate paths
    :param csv_kwargs: parameters for csv parsing
    :return: Paths generated from data and the unique values seen in each path_indicator column
    """
    csv_kwargs = {"skipinitialspace": True} | csv_kwargs
    df = pd.read_csv(infile, **csv_kwargs)
    assert energy in df.columns
    assert name in df.columns
    df.rename(columns={energy: "energy", name: "name"}, inplace=True)
    df = df.convert_dtypes(infer_objects=True)

    if path_indicators == "r-groups":
        path_indicators = find_r_groups(df)
    else:
        for indicator in path_indicators:
            assert indicator in df.columns
    df.sort_values(list(path_indicators) + ["step"], inplace=True)

    paths = read_paths(df, path_indicators)
    pi_dict = {indicator: tuple(df[indicator].unique()) for indicator in path_indicators}

    return paths, pi_dict


def read_paths(df: pd.DataFrame, path_indicators: Sequence[str]) -> dict[tuple[str, ...], Path]:
    """
    Read data into separate paths, named by the group
    """
    return {
        names: pathify(path_data, str(names))  # keep open
        for names, path_data in df.groupby(list(path_indicators))  # keep open
    }


def pathify(data: pd.DataFrame, name: str = "") -> Path:
    """
    Reads DataFrame and converts to a Path

    Notes:
        Assumes all data is sequential and part of the same path
        Does not currently utilize step data to combine molecules on the same step
    :param data: Path data
    :param name: Name for the Path
    """
    molecules = [Molecule(name, energy) for name, energy in zip(data["name"], data["energy"])]
    reactions = [Reaction([reactant], [product]) for reactant, product in mit.windowed(molecules, 2)]  # type:ignore
    return Path(reactions, name)


def find_r_groups(data: pd.DataFrame) -> list[str]:
    """
    Find all of the r-groups in DataFrame columns with form: r#
    """
    return natsorted(name for name in data.columns if name[0] == "r" and name[1:].isnumeric())
