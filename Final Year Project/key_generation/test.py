import numpy as np
a1 = np.array([1,1])
a2 = np.array([1,1])
a3 = np.array([1,1])

a4 = np.array([a1,a2,a3])
total = sum(i for i in a4)
print(total)