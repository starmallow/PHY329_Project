# Demonstrates the models with varied car density, randomization factors, and traffic lanes

import sys
sys.path.append('../code/')

from nsmodel import *

import numpy as np
import matplotlib.pyplot as plt

timesteps = 100
cars = 15
cells = 100

test2 = TrafficModelCircular(cars, cells)
test2.simulate(timesteps)
data = test2.history

fig, ax = plt.subplots(figsize=(12, timesteps//10), dpi=300)
im = ax.imshow(data, cmap='Greys')

# ax.set_xticks([])
# ax.set_yticks([])
ax.tick_params(axis='x', labelsize=8)
ax.tick_params(axis='y', labelsize=8)

ax.set_ylabel("Timestep", fontsize=12)
ax.set_xlabel("Cell Index", fontsize=12)
ax.set_title("Time Evolution of Single, Circular Traffic Lane", fontsize=14)
cbar = plt.colorbar(im, ax=ax, pad=0.02)
cbar.set_label(f"Car Velocity\n(-1 indicates no cars present)", fontsize=10, labelpad=1)

plt.show()
