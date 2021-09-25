#!/usr/bin/python3

from math import sqrt

l1 = float(input('lambda 1: '))
l2 = float(input('lambda 2: '))
l3 = float(input('lambda 3: '))

#FA
fa = sqrt(1/2) * sqrt((l1-l2)**2+(l1-l3)**2+(l2-l3)**2) / sqrt(l1**2 + l2**2 + l3**2)

fa_f='{:.2f}'.format(fa)


print("FA=" + fa_f)

#https://stackoverflow.com/questions/7819498/plotting-ellipsoid-with-matplotlib
import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ellispsoid and center in matrix form
A = np.array([[l1,0,0],[0,l2,0],[0,0,l3]])
center = [0,0,0]

# find the rotation matrix and radii of the axes
U, s, rotation = linalg.svd(A)
radii = 1.0/np.sqrt(s)

# now carry on with EOL's answer
u = np.linspace(0.0, 2.0 * np.pi, 100)
v = np.linspace(0.0, np.pi, 100)
x = radii[0] * np.outer(np.cos(u), np.sin(v))
y = radii[1] * np.outer(np.sin(u), np.sin(v))
z = radii[2] * np.outer(np.ones_like(u), np.cos(v))
for i in range(len(x)):
    for j in range(len(x)):
        [x[i,j],y[i,j],z[i,j]] = np.dot([x[i,j],y[i,j],z[i,j]], rotation) + center

# plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(x, y, z,  rstride=4, cstride=4, color='b', alpha=0.2)
plt.show()
plt.close(fig)
del fig

