from reaction_web.web import Web
from reaction_web.path import Path
from reaction_web.molecule import Molecule
from reaction_web.reaction import EReaction, Reaction

import matplotlib.pyplot as plt


proton = Molecule('H+', 1, 1)
hydrogen_atom = Molecule('H', 0, 2)
hydrogen_molecule = Molecule('H2', -1, 1)
oxygen_atom = Molecule('O', 0, 3)
water = Molecule('H2O', -2, 1)

print(proton)
print(hydrogen_atom)
print(hydrogen_molecule)

# H+ + e- -> H (potential of -1.5)
r1 = EReaction([proton], [hydrogen_atom], ne=1, ref_pot=-1.5)
print(r1)
# H + H -> H2
r2 = Reaction([hydrogen_atom]*2, [hydrogen_molecule])
print(r2)
# H2 + O -> H2O
r3 = Reaction([hydrogen_molecule, oxygen_atom], [water])
print(r3)

# Water production
# H + H -> H2
# H2 + O -> H2O
p1 = Path([r2, r3])
print(p1)
print(p1.energies)
p1.plot()
plt.show()

# H+ + e- -> H
# H + H -> H2
p2 = Path([r1, r2])
print(p2)
print(p2.energies)
p2.plot()
plt.show()

# Both reactions on same plot
web = Web([p1, p2])
print(web)
web.plot()
plt.legend(['Water production', 'Hydrogen production from proton'])
plt.show()
