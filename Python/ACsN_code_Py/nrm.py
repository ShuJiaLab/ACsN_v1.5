import numpy as np
from numba import jit, njit, cuda

@njit
def nrm(n):
    n = np.asarray(n, dtype=np.float)

    in_max = n
    in_min = n

    for i in range(0, n.ndim):
        in_max = max(in_max)
        in_min = min(in_min)

    out = (n - in_min)/(in_max - in_min)

    return out