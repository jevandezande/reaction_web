from typing import Literal, Sequence

import matplotlib.pyplot as plt
import more_itertools as mit
import numpy as np

from .. import Enumeration, Path, Web, translate
from .._typing import PLOT


def gen_plot(
    steps: int,
    title: str = "",
    xlabel: str = "Species",
    ylabel: str = "Energy",
    xtickslabels: Sequence[str] | None = None,
) -> PLOT:
    """
    Generates a plot

    :param steps: number of steps (reactions)
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param xtickslabels: labels for the x-ticks
    """
    fig, ax = plt.subplots()

    if title:
        fig.suptitle(title)

    ax.set_xticks(np.arange(steps + 1))
    ax.set_xlabel(xlabel)

    if xtickslabels:
        assert len(xtickslabels) == steps + 1
        ax.set_xticklabels(xtickslabels)

    ax.set_ylabel(ylabel)

    return fig, ax


def plot_path(
    path: Path,
    title: str = "",
    plot: PLOT | None = None,
    spread: float | bool = True,
    xtickslabels: Sequence[str] | None = None,
    latexify: bool = True,
) -> PLOT:
    """
    Plot of the reaction Path

    :param path: Path to plot
    :param title: title for the plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param spread: how much to spread the connecting lines
    :param xtickslabels: labels for the xticks (replaces numbers)
    :param latexify: convert names to latex
    """
    if not xtickslabels:
        xtickslabels = list(map(str, range(len(path) + 1)))

    fig, ax = plot or gen_plot(len(path), title, xtickslabels=xtickslabels)

    spread_width = 0.1 if spread is True else float(spread)

    length = len(path) + 1

    xs = np.repeat(np.arange(length), 2) + [-0.5 + spread_width, 0.5 - spread_width] * length
    xs[2:] += np.repeat(np.cumsum(path.steps), 2)

    # swap if going backwards
    for i in np.where(path.steps < 0)[0] * 2 + 2:
        xs[[i + 1, i]] = xs[[i, i + 1]]

    ys = np.append([0, 0], np.repeat(np.cumsum(path.energies), 2))

    label = translate(path.name) if latexify else path.name
    ax.plot(xs, ys, label=label)

    return fig, ax


def plot_web(
    web: Web,
    title: str = "",
    plot: PLOT | None = None,
    style: Literal["stacked", "subplots"] = "stacked",
    spread: float | bool = True,
    xtickslabels: Sequence[str] | None = None,
    latexify: bool = True,
) -> PLOT:
    """
    Plot the reaction Paths in a Web.

    :param web: Web to plot
    :param title: title for the plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param style: style of plots:
        stacked: all paths on the same plot
        subplots: each path in its own subplot
    :param spread: how much to spread the connecting lines
    :param xtickslabels: labels for the xticks (replaces numbers)
    :param latexify: convert names to latex
    """
    max_len = max(len(path) for path in web)
    if not xtickslabels:
        xtickslabels = list(map(str, range(max_len + 1)))

    if not plot:
        if style == "stacked":
            fig, axes = gen_plot(max_len, title, xtickslabels=xtickslabels)
            axes_flat = [axes] * len(web)

        elif style == "subplots":
            height = int(np.sqrt(len(web)))
            width = -(len(web) // -height)  # Ceiling integer division

            fig, axes = plt.subplots(height, width, sharex=True, sharey=True)
            fig.subplots_adjust(hspace=0, wspace=0)

            if title:
                fig.suptitle(title)

            axes_flat = list(mit.collapse(axes))  # type: ignore

            axes_flat[0].set_xticks(np.arange(max_len + 1))
            if xtickslabels:
                axes_flat[-1].set_xticklabels(xtickslabels)

            axes_flat[0].set_ylabel("Energy")

    else:
        fig, axes = plot
        axes_flat = [axes] * len(web)

    for path, ax in zip(web, axes_flat):
        plot_path(path, plot=(fig, ax), spread=spread, latexify=latexify)
        ax.legend()
        ax.set_xlabel("Species")

    if plot and title:
        plot[1].set_title(title)

    return fig, axes


def plot_enumeration(
    enm: Enumeration,
    title: str = "",
    plot: PLOT | None = None,
    style: Literal["stacked", "subplots"] = "stacked",
    spread: float | bool = True,
    xtickslabels: Sequence[str] | None = None,
    latexify: bool = True,
    top_level: bool = True,
) -> PLOT:
    """
    Plot the reaction Paths in a Web.

    :param web: Web to plot
    :param title: title for the plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param style: style of plots:
        stacked: all paths on the same plot
        subplots: each path in its own subplot
    :param spread: how much to spread the connecting lines
    :param xtickslabels: labels for the xticks (replaces numbers)
    :param latexify: convert names to latex
    """
    if not xtickslabels:
        xtickslabels = list(map(str, range(len(enm) + 1)))

    if style != "stacked":
        raise NotImplementedError()

    fig, ax = plot or gen_plot(len(enm), title, xtickslabels=xtickslabels)

    if plot and title:
        plot[1].set_title(title)

    if enm.ndim == 1:
        for path in enm:
            assert isinstance(path, Path)
            plot_path(path, plot=(fig, ax), spread=spread, latexify=latexify)
    else:
        for sub_enm in enm:
            assert isinstance(sub_enm, Enumeration)
            plot_enumeration(sub_enm, plot=(fig, ax), style=style, spread=spread, latexify=latexify, top_level=False)

    if top_level:
        ax.set_xlabel("Species")
        ax.legend()

    return fig, ax
