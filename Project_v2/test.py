import numpy as np

x = np.arange(0,100.5,0.5)
y=10+(1/10000000)*(x)**4

for s in y:
    print(str(round(s, 5)) + ',', end="")

print("")

for s in y:
    print(str(round(s+5, 5)) + ',', end="")

print("")

for s in x:
    print(str(round(s, 5)) + ',', end="")