from blochVector import BlochVector
import numpy as np


vector = BlochVector(2*np.pi)
vector.rotate(np.pi/4, 0.25)

vector.display()