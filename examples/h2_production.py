import matplotlib.pyplot as plt

from reaction_web import EReaction, Molecule, Path, Reaction, Web, diagram, heatmap

proton = Molecule("H+", 1)
H = Molecule("H", 0)
H2 = Molecule("H2", -1)
O = Molecule("O", 0)  # noqa: E741
H2O = Molecule("H2O", -2)

print(
    f"""\
Proton        : {proton}
Hydrogen atom : {H}
Hydrogen mol  : {H2}
"""
)

# H+ + e- -> H (potential of -1.5)
r1 = EReaction([proton], [H], ne=1, ref_pot=-1.5)
# H + H -> H2
r2 = Reaction([H] * 2, [H2])
# H2 + O -> H2O
r3 = Reaction([H2, O], [H2O])
print(
    f"""\
Reaction 1: {r1}
Reaction 2: {r2}
Reaction 3: {r3}
"""
)

# Water production
# H + H -> H2
# H2 + O -> H2O
p1 = Path([r2, r3], "Water Production")
print(
    f"""\
Path 1:
{p1}
Energies: {p1.energies}
"""
)
_, ax = diagram.plot_path(p1)
ax.legend()
plt.show()

# H+ + e- -> H
# H + H -> H2
p2 = Path([r1, r2], "H2 Production")
print(
    f"""\
Path 2:
{p2}
Energies: {p2.energies}
"""
)
_, ax = diagram.plot_path(p2)
ax.legend()
plt.show()

# Both reactions on same plot
web = Web([p1, p2])
print(
    f"""\
Web
---
{web}
"""
)
diagram.plot_web(web)
plt.show()

heatmap.heatmap_web(web)
plt.show()
