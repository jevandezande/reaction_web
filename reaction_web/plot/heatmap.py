from typing import Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np

from .. import Path, Web, translate
from .._typing import PLOT


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
    :param rotate_ylabels: rotate labels on y-axis
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


def heatmap_path(
    path: Path,
    title: str = "",
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate a heatmap for a Path

    :param path: Path to plot
    :param title: title for plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param xtickslabels: labels for the x-ticks
    :param showvals: show cell values on the heatmap
    :param cmap: colormap for heatmap
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
    :param title: title for plot
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

    :param webs: Webs to plot
    :param title: title for plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param xtickslabels: labels for the x-ticks
    :param ytickslabels: labels for the y-ticks
    :param rotate_ylabels: rotate labels on y-axis
    :param showvals: show cell values on the heatmap
    :param cmap: colormap for heatmap
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
