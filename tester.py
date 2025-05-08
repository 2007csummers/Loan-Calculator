import loans
import matplotlib.pyplot as mpl
import numpy as np
import math

l1 = loans.loans(40000, .075, 10, False, 12, 2025.75, 54, True)
l2 = loans.loans(200000, .08, 10, False, 12, 2026.0, 51, True)

l1.accrue_lifetime()
l2.accrue_lifetime()




mpl.style.use("_mpl-gallery")

fig, ax = mpl.subplots()

x1=[]
y1=[]
for key in l1.principal_ot:
    x1.append(key)
    y1.append(l1.principal_ot[key])

x2=[]
y2=[]
for key in l2.principal_ot:
    x2.append(key)
    y2.append(l2.principal_ot[key])


ax.plot(x1, y1, ".-b", linewidth=2.0)
ax.plot(x2, y2, ".-r", linewidth=2.0)

ax.set(xlim=(math.trunc(l1.start_year), max(max(l1.interest_ot.keys()), max(l2.interest_ot.keys()))), xticks=np.arange(math.trunc(l1.start_year), max(max(l1.interest_ot.keys()), max(l2.interest_ot.keys()))), 
        ylim=(0, max(max(list(l1.principal_ot.values())), max(list(l2.principal_ot.values()))) + 10000), yticks=np.arange(0, max(max(list(l1.principal_ot.values())), max(list(l2.principal_ot.values()))) + 10000, 10000))


mpl.show()