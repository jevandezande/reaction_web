from typing import Literal, Optional, Sequence

import matplotlib.pyplot as plt
import more_itertools as mit
import numpy as np

from . import Path, Web, translate
from ._typing import PLOT


def gen_plot(
    steps: int,
    title: str = "",
    xlabel: str = "Species",
    ylabel: str = "Energy",
    xtickslabels: Optional[Sequence[str]] = None,
) -> PLOT:
    """
    Generates a plot

    :param steps: number of steps
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
        ax.set_xticklabels(xtickslabels)

    ax.set_ylabel(ylabel)

    return fig, ax


def gen_heatmap_plot(
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    xtickslabels: Optional[Sequence[str]] = None,
    ytickslabels: Optional[Sequence[str]] = None,
    rotate_ylabels: bool = False,
) -> PLOT:
    """
    Generates a heatmap plot

    :param title: title for the plot
    :param xlabel, ylabel: label for the x-axis, y-axis
    :param xtickslabels, ytickslabels: labels to the x-ticks, y-ticks
    """
    fig, ax = plt.subplots()

    if title:
        fig.suptitle(title)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if xtickslabels:
        ax.set_xticks(np.arange(len(xtickslabels)), xtickslabels)
    if ytickslabels:
        ax.set_yticks(np.arange(len(ytickslabels)), ytickslabels, rotation=90 * rotate_ylabels, va="center")

    return fig, ax


def plot_path(
    path: Path,
    title: str = "",
    plot: Optional[PLOT] = None,
    spread: float | bool = True,
    xtickslabels: Optional[Sequence[str]] = None,
    latexify: bool = True,
) -> PLOT:
    """
    Plot of the reaction path

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
    plot: Optional[PLOT] = None,
    style: Literal["stacked", "subplots"] = "stacked",
    spread: float | bool = True,
    xtickslabels: Optional[Sequence[str]] = None,
    latexify: bool = True,
) -> PLOT:
    """
    Plot the reaction paths.

    :param style: style of plots:
        stacked: all paths on the same plot
        subplots: each path in its own subplot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
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

            axes_flat = list(mit.collapse(axes))

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


def heatmap_path(
    path,
    title: str = "",
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate a heatmap for a path
    """
    energies = path.energies

    if not xtickslabels:
        xtickslabels = list(map(str, range(len(path) + 1)))

    fig, ax = plot or gen_heatmap_plot(title, "Species", xtickslabels=xtickslabels, ytickslabels=[""])

    ax.imshow([energies], cmap)

    if showvals:
        for i, val in enumerate(energies):
            ax.text(i, 0, f"{val:.1f}", ha="center", va="center")

    return fig, ax


def heatmap_web(
    web: Web,
    title: str = "",
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    ytickslabels: Optional[Sequence[str]] = None,
    rotate_ylabels: bool = True,
    showvals: bool = False,
    cmap="coolwarm",
    latexify: bool = True,
) -> PLOT:
    """
    Generate heatmaps for all paths in Web

    :param web: Web to plot
    :param title: Title for plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param xtickslabels: labels for the x-ticks
    :param ytickslabels: labels for the y-ticks
    :param rotate_ylabels: rotate labels on y-axis
    :param showvals: show cell values on the heatmap
    :param cmap: colormap for heatmap
    :param latexify: convert names to latex
    """
    web_length = len(web.paths[0])
    if not all(web_length == len(p) for p in web.paths):
        raise ValueError("Can only plot paths with consistent path lengths.")

    data = np.array([path.energies for path in web])

    if not xtickslabels:
        xtickslabels = list(map(str, range(web_length + 1)))
    if not ytickslabels:
        ytickslabels = [(translate(path.name) if latexify else path.name) for path in web]

    fig, ax = plot or gen_heatmap_plot(title, "Species", "Paths", xtickslabels, ytickslabels, rotate_ylabels)

    if title:
        fig.suptitle(title)

    ax.imshow(data, cmap)

    if showvals:
        for (j, i), val in np.ndenumerate(data):
            ax.text(i, j, f"{val:.1f}", ha="center", va="center")

    return fig, ax


def heatmap_webs_max(
    webs: Sequence[Web],
    title: str = "",
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    ytickslabels: Optional[Sequence[str]] = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from the max of each Path in the Webs.
    """
    length = len(webs[0])
    if not all(length == len(web) for web in webs):
        raise ValueError("Can only plot Webs with the same number of Paths")

    data = np.array([[path.max()[1] for path in web] for web in webs])

    if not xtickslabels:
        xtickslabels = list(map(str, range(length + 1)))
    if not ytickslabels:
        ytickslabels = list(map(str, range(len(webs) + 1)))

    fig, ax = plot or gen_heatmap_plot(title, "R1", "R2", xtickslabels, ytickslabels, rotate_ylabels)

    ax.imshow(data, cmap)

    if showvals:
        for (j, i), val in np.ndenumerate(data):
            ax.text(i, j, f"{val:.1f}", ha="center", va="center")

    return fig, ax
