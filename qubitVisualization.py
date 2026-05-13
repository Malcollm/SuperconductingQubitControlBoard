from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
from blochVector import BlochVector
import numpy as np


vector = BlochVector(2*np.pi)
plot_bloch_vector(vector.get_state(), title="Bloch Sphere")
vector.rotate(np.pi/4, 0.25)
plot_bloch_vector(vector.get_state(), title="Bloch Sphere")

plt.show()