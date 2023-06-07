import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots
from pytest import fixture, mark, raises

from reaction_web import EReaction, Molecule, Path, Reaction, Web
from reaction_web.plot.heatmap import (
    gen_subplots,
    heatmap_enumeration_function,
    heatmap_path,
    heatmap_web,
    heatmap_webs_function,
    heatmap_webs_max,
    heatmap_webs_min,
    heatmap_webs_relative_step,
    heatmap_webs_step,
)
from reaction_web.tools.generate_paths import enumeration_factory

pytestmark = mark.graphical


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


@fixture
def web_list(web):
    path1, path2, path3 = web
    return [web, Web([path2, path3, path1])]


def test_heatmap_path(web):
    path1, path2, path3 = web

    fig, (ax1, ax2, ax3) = subplots(3)

    heatmap_path(path1, plot=(fig, ax1))
    heatmap_path(path2, plot=(fig, ax2))
    heatmap_path(path3, plot=(fig, ax3), showvals=True)
    plt.close()


def test_heatmap_web(web):
    _, path2, path3 = web
    web2 = Web([path2, path3])

    heatmap_web(web2, title="Test", showvals=True)
    plt.close()


def test_heatmap_webs_function(web_list):
    def path_min(path: Path) -> float:
        return path.min()[0]

    heatmap_webs_function(web_list, path_min)
    plt.close()


def test_heatmap_webs_max(web_list):
    heatmap_webs_max(web_list, xtickslabels=[1, 2, 3], ytickslabels=["A", "B"], showvals=True)
    plt.close()

    web3 = Web(list(web_list[0])[:2])
    with raises(ValueError):
        heatmap_webs_max(web_list + [web3])


def test_heatmap_webs_min(web_list):
    heatmap_webs_min(web_list)
    plt.close()


def test_heatmap_webs_step(web_list):
    heatmap_webs_step(web_list, 1)
    plt.close()


def test_heatmap_webs_relative_step(web_list):
    heatmap_webs_relative_step(web_list, 1)
    plt.close()


@mark.parametrize(
    "shape",
    [
        tuple(),
        (1,),
        (5,),
        (2, 3),
        (1, 1, 1),
        (2, 3, 4, 1),
        (3, 1, 2, 4, 5),
    ],
)
def test_gen_subplots(shape):
    fig, axes, gs = gen_subplots(shape)
    assert axes.shape == shape

    plt.close()


@mark.parametrize(
    "shape,labels",
    [
        [tuple(), None],
        [(1,), (("A",),)],
        [(5,), ("ABCDE",)],
        [(2, 3), (("A", "B"), ("C", "C", "C"))],
        [(1, 1, 1), ("A", "B", "C")],
        [(2, 3, 4, 1), ("AB", "CDE", "FGHI", "K")],
        [(3, 1, 2, 4, 5), ("ABC", "D", "EF", "GHIJ", "KLMNO")],
    ],
)
def test_gen_subplots_labels(shape, labels):
    fig, axes, gs = gen_subplots(shape, labels=labels)
    assert axes.shape == shape

    plt.close()


def test_heatmap_enumeration_function():
    enm = enumeration_factory("tests/data/enum_2_3_2_3_4.csv")
    fig, ax = heatmap_enumeration_function(enm, lambda path: path.max()[1], showvals=True)

    plt.close()
