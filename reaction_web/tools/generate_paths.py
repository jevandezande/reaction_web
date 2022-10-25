from typing import Sequence

import more_itertools as mit
import pandas as pd
from natsort import natsorted

from .. import Molecule, Path, Reaction


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
    paths: Sequence[str] | str = "r-groups",
    **csv_kwargs,
) -> dict[str, Path]:
    """
    Read molecule data in a CSV and convert into paths

    Note:
        Only utilizes step data to sort, no combination yet available

    :param infile: file to read
    :param energy: column to use for molecule energy
    :param name: column to use for molecule name
    :param csv_kwargs: parameters for csv parsing
    :return: Paths generated from data
    """
    csv_kwargs = {"skipinitialspace": True} | csv_kwargs
    df = pd.read_csv(infile, **csv_kwargs)
    df.rename(columns={energy: "energy", name: "name"}, inplace=True)
    df = df.convert_dtypes(infer_objects=True)

    if paths == "r-groups":
        paths = find_r_groups(df)
    else:
        for path in paths:
            assert path in df.columns
    df.sort_values(list(paths) + ["step"], inplace=True)

    return read_paths(df, paths)


def read_paths(df: pd.DataFrame, paths: Sequence[str]) -> dict[str, Path]:
    """
    Read data into separate paths, named by the group
    """
    return {
        str(r_group): pathify(path_data, str(r_group))  # keep open
        for r_group, path_data in df.groupby(paths)  # keep open
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
    reactions = [Reaction([reactant], [product]) for reactant, product in mit.windowed(molecules, 2)]
    return Path(reactions, name)


def find_r_groups(data: pd.DataFrame) -> list[str]:
    """
    Find all of the r-groups in DataFrame columns with form: r#
    """
    return natsorted(name for name in data.columns if name[0] == "r" and name[1:].isnumeric())
