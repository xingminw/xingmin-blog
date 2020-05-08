import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pydmd import DMD


def f1(x, t):
    return 1. / np.cosh(x + 3) * np.exp(2.3j * t)


def f2(x, t):
    return 2. / np.cosh(x) * np.tanh(x) * np.exp(2.8j * t)


x = np.linspace(-5, 5, 128)
t = np.linspace(0, 4 * np.pi, 256)
xgrid, tgrid = np.meshgrid(x, t)

X1 = f1(xgrid, tgrid)
X2 = f2(xgrid, tgrid)
X = X1 + X2

# PCA (SVD)
U, s, V = np.linalg.svd(X.T)
rank = 2
plt.figure()
plt.subplot(221)
for r in range(rank):
    plt.plot(U[:, r], "-")
plt.title("Column vectors of U (Modes)")
plt.subplot(222)
for r in range(rank):
    plt.plot(V[r, :], "-")
plt.title("Row vectors of V (Dynamics)")
plt.subplot(223)
plt.plot(s, ".-")
plt.xlim([0, 10])
plt.title("Singular values")

plt.show()

dmd = DMD(svd_rank=2)
dmd.fit(X.T)
modes = dmd.modes.T.real
plt.figure()

plt.subplot(121)
for mode in dmd.modes.T:
    plt.plot(x, mode.real)
    plt.title('Modes')

plt.subplot(122)
for dynamic in dmd.dynamics:
    plt.plot(t, dynamic.real)
    plt.title('Dynamics')

print(dmd.frequency)
plt.show()

plt.figure()
plt.subplot(221)
plt.title("Input modes")
plt.plot(X1[0], "-")
plt.plot(X2[0], "-")

plt.subplot(222)
plt.title("Input dynamics")
plt.plot([val[0] / X1[0][0] for val in X1])
plt.plot([val[10] / X2[0][10] for val in X2])

plt.subplot(223, projection="3d").plot_surface(xgrid, tgrid, np.real(X1), rstride=1, cstride=1,
                                               cmap='viridis', edgecolor='none')
plt.title("Mode 1")

# ax.plot_surface(X, Y, mode1_series)
plt.subplot(224, projection="3d").plot_surface(xgrid, tgrid, np.real(X2), rstride=1, cstride=1,
                                               cmap='viridis', edgecolor='none')
plt.title("Mode 2")
plt.show()

plt.figure()
ax = plt.gca(projection="3d")
ax.plot_surface(xgrid, tgrid, np.real(X), rstride=1, cstride=1, cmap='viridis', edgecolor='none')
plt.show()
