import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots
from pytest import fixture

from reaction_web import EReaction, Molecule, Path, Reaction, Web
from reaction_web.plot import heatmap_path, heatmap_web, heatmap_web_max, plot_path, plot_web


@fixture
def web():
    refp = 5
    a = Molecule("a", 1)
    b = Molecule("b", 0)
    c = Molecule("c", 2)
    d = Molecule("d", -1)
    e = Molecule("e", 3)
    f = Molecule("f", 0.5)
    r1 = Reaction([a], [b])
    r2 = Reaction([b], [c])
    r3 = Reaction([c], [d, e])
    r4 = EReaction([e], [f], ne=1, ref_pot=refp)
    path1 = Path([r1, r2, r3, r4], "P1")
    path2 = Path([r2, r3, r4], "P2")
    path3 = Path([r2, r3, r4], "", step_sizes=[2, -1, 3])

    return Web([path1, path2, path3])


def test_plot_path(web):
    path1, path2, path3 = web
    plot_path(path1, plot=subplots())
    plot_path(path2, spread=False, xtickslabels=("R", "TS", "I", "P"))
    plot_path(path3, latexify=False)


def test_plot_web(web):
    plot_web(web, plot=subplots())
    plot_web(web, style="subplots")
    plot_web(web, style="stacked")


def test_heatmap_path(web):
    path1, path2, path3 = web

    fig, (ax1, ax2, ax3) = plt.subplots(3)

    heatmap_path(path1, plot=(fig, ax1))
    heatmap_path(path2, plot=(fig, ax2))
    heatmap_path(path3, plot=(fig, ax3))


def test_heatmap_web(web):
    path1, path2, path3 = web
    web2 = Web([path2, path3])

    heatmap_web(web2)


def test_heatmap_web_max(web):
    path1, path2, path3 = web

    heatmap_web_max(web)
