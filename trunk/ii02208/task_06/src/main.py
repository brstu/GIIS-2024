import numpy as np
import matplotlib.pyplot as plt
from delaunay import Delaunay2D

seed_count = 6

seeds = np.random.random((seed_count, 2))
start_cords = [(-1, -1), (+1, -1), (+1, +1), (-1, +1)]
Z =  [(_[1] - _[0] + 1) / 5 for _ in start_cords + list(seeds)]

dt = Delaunay2D()
for s in seeds:
    dt.addPoint(s)

center = np.mean(seeds, axis=0)
radius = np.max(np.linalg.norm((seeds - center), axis=1))
dt = Delaunay2D(center, 2 * radius)
perm = sorted(range(len(seeds)), key=lambda i: seeds[i][0])
for i in perm:
    dt.addPoint(seeds[i])

coords, triangles = dt.exportExtendedDT()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(seeds[:, 0], seeds[:, 1], Z[4:], color='blue', label='Points')

for triangle in triangles:
    x = [coords[pt][0] for pt in triangle]
    y = [coords[pt][1] for pt in triangle]
    z = [Z[pt] for pt in triangle]
    ax.plot(x, y, zs=z, color='red')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Delaunay Triangulation')
ax.legend()
ax.grid(True)
plt.show()