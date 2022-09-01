from typing import Iterable, Literal, Optional, Sequence

import matplotlib.pyplot as plt
import more_itertools as mit
import numpy as np

from . import Path, Web, translate
from ._typing import PLOT


def gen_plot(
    steps: int,
    xlabel: str = "Species",
    ylabel: str = "Energy",
    xtickslabels: Optional[list[str]] = None,
) -> PLOT:
    """
    Generates a plot

    :param steps: number of steps
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    """
    fig, ax = plt.subplots()

    ax.set_xticks(np.arange(steps + 1))
    ax.set_xlabel(xlabel)

    if xtickslabels:
        ax.set_xticklabels(xtickslabels)

    ax.set_ylabel(ylabel)

    return fig, ax


def plot_path(
    path: Path,
    plot: Optional[PLOT] = None,
    spread: float | bool = True,
    xtickslabels: Optional[list[str]] = None,
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
    fig, ax = plot if plot else gen_plot(len(path))

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
    title: Optional[str] = None,
    style: Literal["stacked", "subplots"] = "stacked",
    plot: Optional[PLOT] = None,
    spread: float | bool = True,
    xtickslabels: Optional[list[str]] = None,
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

    if not plot:
        if style == "stacked":
            fig, axes = gen_plot(max_len, xtickslabels=xtickslabels)
            axes_flat = [axes] * len(web)

        elif style == "subplots":
            height = int(np.sqrt(len(web)))
            width = -(len(web) // -height)  # Ceiling integer division

            fig, axes = plt.subplots(height, width, sharex=True, sharey=True)
            fig.subplots_adjust(hspace=0, wspace=0)
            axes_flat = list(mit.collapse(axes))

            if xtickslabels:
                axes_flat[0].set_xticks(np.arange(max_len + 1))
                axes_flat[-1].set_xticklabels(xtickslabels)

            axes_flat[0].set_ylabel("Energy")

    else:
        fig, axes = plot
        axes_flat = [axes] * len(web)

    for path, ax in zip(web, axes_flat):
        plot_path(path, plot=(fig, ax), spread=spread, latexify=latexify)
        ax.legend()
        ax.set_xlabel("Species")

    if title:
        if plot:
            plot[1].set_title(title)
        else:
            fig.suptitle(title)

    return fig, axes


def heatmap_path(
    path,
    title: Optional[str] = None,
    plot: Optional[PLOT] = None,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate a heatmap for a path
    """
    data = [path.energies]

    fig, ax = plot or plt.subplots()

    if title:
        fig.suptitle(title)

    ax.imshow(data, cmap)

    return fig, ax


def heatmap_web(
    web: Web,
    title: Optional[str] = None,
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
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
    :param cmap: colormap for heatmap
    :param latexify: convert names to latex
    :param rotate_ylabels: rotate labels on y-axis
    """
    if not all(len(web.paths[0]) == len(p) for p in web.paths):
        raise ValueError("Can only plot paths with consistent path lengths.")

    data = [path.energies for path in web]

    fig, ax = plot or plt.subplots()

    ax.set_xlabel("Species")
    ax.set_ylabel("Paths")

    ax.set_xticks(np.arange(len(web.paths[0]) + 1))
    if xtickslabels:
        ax.set_xticklabels(xtickslabels)

    ylabels = [(translate(path.name) if latexify else path.name) for path in web]
    ax.set_yticks(np.arange(len(web)), ylabels, rotation=90 * rotate_ylabels, va="center")

    if title:
        fig.suptitle(title)

    ax.imshow(data, cmap)

    if showvals:
        for (j, i), val in np.ndenumerate(data):
            ax.text(i, j, f"{val:.1f}", ha="center", va="center")

    return fig, ax


def heatmap_webs_max(
    webs: Iterable[Web],
    title: Optional[str] = None,
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    ytickslabels: Optional[Sequence[str]] = None,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from the max of each Path in the Web.
    """
    data = np.array([[path.max()[1] for path in web] for web in webs])

    fig, ax = plot or plt.subplots()

    if title:
        fig.suptitle(title)

    ax.imshow(data, cmap)

    if xtickslabels:
        ax.set_xticks(np.arange(len(xtickslabels)))
        ax.set_xticklabels(xtickslabels)

    if ytickslabels:
        ax.set_yticks(np.arange(len(ytickslabels)))
        ax.set_yticklabels(ytickslabels)

    if showvals:
        for (j, i), val in np.ndenumerate(data):
            ax.text(i, j, f"{val:.1f}", ha="center", va="center")

    return fig, ax
