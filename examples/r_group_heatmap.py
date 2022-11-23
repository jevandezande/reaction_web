import matplotlib.pyplot as plt

from reaction_web import Path, heatmap
from reaction_web.tools.generate_paths import enumeration_factory

enm = enumeration_factory("tests/data/enum_3_4_3.csv")


def max_energy(path: Path) -> float:
    return path.max()[1]


def step_energy(path: Path) -> float:
    return path[0].energy


heatmap.heatmap_enumeration_function(enm, max_energy, showvals=True)
plt.show()
