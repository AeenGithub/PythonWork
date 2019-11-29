import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-6,6,100)
y = np.sin(x) + 1
z = np.cos(x) 

plt.plot(x, y, 'r', x, z, 'b')
plt.show()
print(np.pi)