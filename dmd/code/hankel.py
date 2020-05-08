import numpy as np


def hankel(x, dim):
    total_dim = np.shape(x)[0]

    hankel_matrix = np.empty((dim, total_dim - dim))
    for idx in range(dim):
        hankel_matrix[idx, :] = x[idx: idx + total_dim - dim]
    return hankel_matrix
