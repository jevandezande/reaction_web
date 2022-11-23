from typing import Callable, Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

from .. import Enumeration, Path, Web, translate
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


def heatmap_webs_function(
    webs: Sequence[Web],
    function: Callable[[Path], float],
    title: str = "",
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    ytickslabels: Optional[Sequence[str]] = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from a value in each Path in the Webs

    Note: each Web is on a different row, with Paths spread across columns

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

    data = np.array([[function(path) for path in web] for web in webs])

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
    Generate heatmap from the max of each Path in the Webs

    Note: each Web is on a different row, with Paths spread across columns

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

    def path_max(path: Path) -> float:
        return path.max()[0]

    return heatmap_webs_function(
        webs, path_max, title, plot, xtickslabels, ytickslabels, rotate_ylabels, showvals, cmap
    )


def heatmap_webs_min(
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
    Generate heatmap from the min of each Path in the Webs

    Note: each Web is on a different row, with Paths spread across columns

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

    def path_min(path: Path) -> float:
        return path.min()[0]

    return heatmap_webs_function(
        webs, path_min, title, plot, xtickslabels, ytickslabels, rotate_ylabels, showvals, cmap
    )


def heatmap_webs_step(
    webs: Sequence[Web],
    step: int,
    title: str = "",
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    ytickslabels: Optional[Sequence[str]] = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from a specific step for each Path in the Webs

    Note: each Web is on a different row, with Paths spread across columns

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

    def path_step(path: Path) -> float:
        return path.energies[step]

    return heatmap_webs_function(
        webs, path_step, title, plot, xtickslabels, ytickslabels, rotate_ylabels, showvals, cmap
    )


def heatmap_webs_relative_step(
    webs: Sequence[Web],
    step: int,
    title: str = "",
    plot: Optional[PLOT] = None,
    xtickslabels: Optional[Sequence[str]] = None,
    ytickslabels: Optional[Sequence[str]] = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from a specific step for each Path in the Webs

    Note: each Web is on a different row, with Paths spread across columns

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

    def path_relative_step(path: Path) -> float:
        return path.relative_energies[step]

    return heatmap_webs_function(
        webs, path_relative_step, title, plot, xtickslabels, ytickslabels, rotate_ylabels, showvals, cmap
    )


def heatmap_enumeration_function(
    enm: Enumeration,
    function: Callable[[Path], float],
    title: str = "",
    plot: PLOT | None = None,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from a value in each Path in the Enumeration

    :param enumeration: Enumeration to plot
    :param title: title for plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param showvals: show cell values on the heatmap
    :param cmap: colormap for heatmap
    """
    fig, axes = plot or gen_subplots(enm.shape[:-2])

    if title:
        fig.suptitle(title)

    if enm.ndim == 1:
        n_heatmaps, m, n = 1, enm.shape[0], 1  # pretend it is 1 x m x 1 in shape
    else:
        assert axes.shape == enm.shape[:-2]
        *head, m, n = enm.shape
        n_heatmaps = int(np.prod(head))  # np.prod returns 1.0 for an empty iterable

    data_l_m_n = np.fromiter(map(function, enm.paths.flat), dtype=float).reshape(n_heatmaps, m, n)
    vmin = data_l_m_n.min()
    vmax = data_l_m_n.max()

    for ax, data in zip(axes.flat, data_l_m_n):
        ax.imshow(data, cmap, vmin=vmin, vmax=vmax)

        if showvals:
            for (j, i), val in np.ndenumerate(data):
                ax.text(i, j, f"{val:.1f}", ha="center", va="center")

    return fig, axes


def gen_subplots(
    shape: Sequence[int],
    fig: plt.Figure | None = None,
    gs: GridSpec | None = None,
) -> PLOT:
    """
    Recursively generate subplots

    >>> gen_subplots((2, 3, 4))[1].shape
    (2, 3, 4)

    Note:
        The last dimension is always a column dimension.
        This enforces a landscape view and simplifies integration with heatmaps.

    :param shape: the n-dimensional shape of the subplots
    :param fig: figure on which to generate the axes
    :param gs: gridspec on which to recurse (typically only use internally)
    """
    ndim = len(shape)
    fig = fig or plt.figure()

    if ndim == 0:
        gs = gs or GridSpec(1, 1, figure=fig)
        return fig, np.array(fig.add_subplot(gs[0]))

    # If odd, only use first dimension
    row_dim, col_dim, *tail = (1, *shape) if ndim % 2 else shape

    gs = gs.subgridspec(row_dim, col_dim) if gs else GridSpec(row_dim, col_dim, figure=fig)

    axes = [[fig.add_subplot(gs[row, col]) for col in range(col_dim)] for row in range(row_dim)]
    if tail:
        axes = [[gen_subplots(tail, fig, gs[row, col])[1] for col in range(col_dim)] for row in range(row_dim)]

    # Squeeze the axes (row_dim == 1)
    if ndim % 2:
        axes = axes[0]

    return fig, np.array(axes)
