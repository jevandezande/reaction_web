from reaction_web import Web
from reaction_web import Path
from reaction_web import Molecule
from reaction_web import EReaction, Reaction

import matplotlib.pyplot as plt

proton = Molecule('H+', 1, 1)
hydrogen_atom = Molecule('H', 0, 2)
hydrogen_molecule = Molecule('H2', -1, 1)
oxygen_atom = Molecule('O', 0, 3)
water = Molecule('H2O', -2, 1)

print(f"""\
Proton        : {proton}
Hydrogen atom : {hydrogen_atom}
Hydrogen mol  : {hydrogen_molecule}
""")

# H+ + e- -> H (potential of -1.5)
r1 = EReaction([proton], [hydrogen_atom], ne=1, ref_pot=-1.5)
# H + H -> H2
r2 = Reaction([hydrogen_atom]*2, [hydrogen_molecule])
# H2 + O -> H2O
r3 = Reaction([hydrogen_molecule, oxygen_atom], [water])
print(f"""\
Reaction 1: {r1}
Reaction 2: {r2}
Reaction 3: {r3}
""")

# Water production
# H + H -> H2
# H2 + O -> H2O
p1 = Path([r2, r3], 'Water Production')
print(f"""\
Path 1:
{p1}
Energies: {p1.energies}
""")
p1.plot()
plt.show()

# H+ + e- -> H
# H + H -> H2
p2 = Path([r1, r2], 'H2 Production')
print(f"""\
Path 2:
{p2}
Energies: {p2.energies}
""")
p2.plot()
plt.show()

# Both reactions on same plot
web = Web([p1, p2])
print(f"""\
Web
---
{web}
""")
web.plot()
plt.show()
