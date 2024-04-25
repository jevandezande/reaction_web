"""Plotting functions for heatmaps of Paths and Webs."""

from typing import Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from numpy.typing import NDArray

from .. import Enumeration, Path, Web, translate
from .._typing import PLOT, Axes, Figure


def gen_heatmap_plot(
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    ytickslabels: Sequence[str | float] | None = None,
    rotate_ylabels: bool = False,
    plot: PLOT | None = None,
) -> PLOT:
    """
    Generate a heatmap plot.

    :param title: title for the plot
    :param xlabel, ylabel: label for the x-axis, y-axis
    :param xtickslabels, ytickslabels: labels to the x-ticks, y-ticks
    :param rotate_ylabels: rotate labels on y-axis
    :param plot: where to plot the Path
    :return: figure and axis
    """
    fig, ax = plot or plt.subplots()

    if title is not None:
        fig.suptitle(title)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if xtickslabels:
        ax.set_xticks(np.arange(len(xtickslabels)), xtickslabels)  # type: ignore
    if ytickslabels:
        ax.set_yticks(
            np.arange(len(ytickslabels)),
            ytickslabels,  # type: ignore
            rotation=90 * rotate_ylabels,
            va="center",
        )

    return fig, ax


def heatmap_path(
    path: Path,
    title: str = "",
    plot: PLOT | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate a heatmap for a Path.

    :param path: Path to plot
    :param title: title for plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param xtickslabels: labels for the x-ticks
    :param showvals: show cell values on the heatmap
    :param cmap: colormap for heatmap
    :return: figure and axis
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
    plot: PLOT | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    ytickslabels: Sequence[str | float] | None = None,
    rotate_ylabels: bool = True,
    showvals: bool = False,
    cmap="coolwarm",
    latexify: bool = True,
) -> PLOT:
    """
    Generate heatmaps for all paths in Web.

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
    :return: figure and axis
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
    plot: PLOT | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    ytickslabels: Sequence[str | float] | None = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from a value in each Path in the Webs.

    Note: each Web is on a different row, with Paths spread across columns

    :param webs: Webs to plot
    :param function: function to apply to each Path
    :param title: title for plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param xtickslabels: labels for the x-ticks
    :param ytickslabels: labels for the y-ticks
    :param rotate_ylabels: rotate labels on y-axis
    :param showvals: show cell values on the heatmap
    :param cmap: colormap for heatmap
    :return: figure and axis
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
    plot: PLOT | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    ytickslabels: Sequence[str | float] | None = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from the max of each Path in the Webs.

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
    :return: figure and axis
    """

    def path_max(path: Path) -> float:
        return path.max()[1]

    return heatmap_webs_function(
        webs,
        path_max,
        title,
        plot,
        xtickslabels,
        ytickslabels,
        rotate_ylabels,
        showvals,
        cmap,
    )


def heatmap_webs_min(
    webs: Sequence[Web],
    title: str = "",
    plot: PLOT | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    ytickslabels: Sequence[str | float] | None = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from the min of each Path in the Webs.

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
    :return: figure and axis
    """

    def path_min(path: Path) -> float:
        return path.min()[1]

    return heatmap_webs_function(
        webs,
        path_min,
        title,
        plot,
        xtickslabels,
        ytickslabels,
        rotate_ylabels,
        showvals,
        cmap,
    )


def heatmap_webs_step(
    webs: Sequence[Web],
    step: int,
    title: str = "",
    plot: PLOT | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    ytickslabels: Sequence[str | float] | None = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from a specific step for each Path in the Webs.

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
    :return: figure and axis
    """

    def path_step(path: Path) -> float:
        return path.energies[step]

    return heatmap_webs_function(
        webs,
        path_step,
        title,
        plot,
        xtickslabels,
        ytickslabels,
        rotate_ylabels,
        showvals,
        cmap,
    )


def heatmap_webs_relative_step(
    webs: Sequence[Web],
    step: int,
    title: str = "",
    plot: PLOT | None = None,
    xtickslabels: Sequence[str | float] | None = None,
    ytickslabels: Sequence[str | float] | None = None,
    rotate_ylabels: bool = False,
    showvals: bool = False,
    cmap="coolwarm",
) -> PLOT:
    """
    Generate heatmap from a specific step for each Path in the Webs.

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
    :return: figure and axis
    """

    def path_relative_step(path: Path) -> float:
        return path.relative_energies[step]

    return heatmap_webs_function(
        webs,
        path_relative_step,
        title,
        plot,
        xtickslabels,
        ytickslabels,
        rotate_ylabels,
        showvals,
        cmap,
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
    Generate heatmap from a value in each Path in the Enumeration.

    :param enumeration: Enumeration to plot
    :param title: title for plot
    :param plot: where to plot the Path
        e.g. using default canvas (plt) or a subplot (the given axis)
    :param showvals: show cell values on the heatmap
    :param cmap: colormap for heatmap
    :return: figure and axis
    """
    labels = list(enm.path_names.values())
    fig, axes = plot or gen_subplots(enm.shape[:-2], labels=labels[:-2])[:2]

    if title:
        fig.suptitle(title)

    if enm.ndim == 1:
        n_heatmaps, m, n = 1, enm.shape[0], 1  # pretend it is 1 x m x 1 in shape
    else:
        assert axes.shape == enm.shape[:-2]  # type: ignore
        *head, m, n = enm.shape
        n_heatmaps = int(np.prod(head))  # np.prod returns 1.0 for an empty iterable

    data_l_m_n = np.fromiter(map(function, enm.paths.flat), dtype=float).reshape(n_heatmaps, m, n)
    vmin = data_l_m_n.min()
    vmax = data_l_m_n.max()

    for ax, data in zip(axes.flat, data_l_m_n):  # type: ignore
        gen_heatmap_plot(xtickslabels=labels[-1], ytickslabels=labels[-2], plot=(fig, ax))
        ax.imshow(data, cmap, vmin=vmin, vmax=vmax)

        if showvals:
            for (j, i), val in np.ndenumerate(data):
                ax.text(i, j, f"{val:.1f}", ha="center", va="center")

    return fig, axes


def gen_subplots(
    shape: Sequence[int],
    fig: Figure | None = None,
    gs: GridSpec | None = None,
    labels: Sequence[Sequence[str]] | None = None,
) -> tuple[Figure, Axes, NDArray[GridSpec]]:  # type: ignore
    """
    Recursively generate subplots.

    >>> gen_subplots((2, 3, 4))[1].shape
    (2, 3, 4)

    Note:
        The last dimension is always a column dimension.
        This enforces a landscape view and simplifies integration with heatmaps.

    :param shape: the n-dimensional shape of the subplots
    :param fig: figure on which to generate the axes
    :param gs: gridspec on which to recurse (typically only use internally)
    :param labels: labels for the axes (matching the dimensions of shape)
    :return: figure, axes, gridspec
    """
    # Sanity check
    if labels:
        assert all(s == len(ls) for s, ls in zip(shape, labels))

    ndim = len(shape)
    fig = fig or plt.figure()

    # Base of recursion
    if ndim == 0:
        gs = gs or GridSpec(1, 1, figure=fig)
        ax = fig.add_subplot(gs[0])
        return fig, np.array(ax), np.array([gs])  # type: ignore

    # If odd, add a shim dimension
    if ndim % 2:
        if labels:
            labels = [[""]] + list(labels)
        row_dim, col_dim, *tail = (1, *shape)
    else:
        row_dim, col_dim, *tail = shape

    gs = gs.subgridspec(row_dim, col_dim) if gs else GridSpec(row_dim, col_dim, figure=fig)  # type: ignore

    # Generate subplots
    axes = np.array([
        [
            fig.add_subplot(gs[row, col])
            for col in range(col_dim)
        ]
        for row in range(row_dim)
    ])  # fmt:skip

    # ylabel on leftmost and xlabel on bottommost
    if labels:
        for ax, ylabel in zip(axes[:, 0], labels[0]):
            ax.set_ylabel(ylabel)
        for ax, xlabel in zip(axes[-1], labels[1]):
            ax.set_xlabel(xlabel)

    # Recurse
    if tail:
        new_axes: list[list[Axes]] = []
        new_gs: list[list[GridSpec]] = []
        sub_labels = labels[2:] if labels else None

        for row, ax_row in enumerate(axes):
            new_axes.append([])
            new_gs.append([])

            for col, ax in enumerate(ax_row):
                remove_frame(ax)

                _, sub_axes, sub_gs = gen_subplots(tail, fig, gs[row, col], sub_labels)  # type: ignore

                new_axes[-1].append(sub_axes)
                new_gs[-1].append(sub_gs)  # type: ignore

        axes = np.array(new_axes)
        gs = np.array(new_gs)  # type: ignore

    # Squeeze, since row_dim == 1 in odd cases
    if ndim % 2:
        axes = axes[0]
        gs = gs[0]  # type: ignore

    return fig, axes, gs  # type: ignore


def remove_frame(ax: Axes) -> None:
    """
    Remove frame and ticks from axis.

    :ax: Axes from which to remove stuff
    """
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
