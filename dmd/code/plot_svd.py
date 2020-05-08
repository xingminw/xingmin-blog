import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_svd(U, s, V):
    rank = 10
    plt.figure(figsize=[12, 8])
    plt.subplot(221)
    for r in range(rank):
        plt.plot(U[:, r], "-")
    plt.title("Column vectors of U")
    plt.subplot(222)
    for r in range(rank):
        plt.plot(V[r, :], "-")
    plt.title("Row vectors of V")
    plt.subplot(223)
    plt.plot(s, "b.-")
    plt.title("Singular values")
    plt.subplot(224, projection="3d")
    plt.plot(V[0, :], V[1, :], V[2, :], lw=0.5)
    plt.title("Trace in new coordinates")
    plt.show()

