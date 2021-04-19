import numpy as np
from numba import jit, njit, cuda
import cupy as cp

# %---------------------------------------------------------%
# %--Gaussian High pass and Low pass filter--------------------%
# %---------------------------------------------------------%

def Gaussian_image_filtering(I, mode = None, r = None):

    R = 10
    Mode = "Gauss"

    if mode != None:
        Mode = mode
    if r != None:
        R = r
    
    A = np.fft.fft2(I)
    A1 = np.fft.fftshift(A)

    M = (A.shape)[0]
    N = (A.shape)[1]
    X = np.arange(N)
    Y = np.arange(M)
    X, Y = np.meshgrid(X, Y)
    Cx = 0.5 * N
    Cy = 0.5 * M

    Lo = np.zeros(A.shape)
    Hi = np.ones(A.shape)
    
    if Mode == 'Gauss':
        Lo = np.exp(-((X-Cx)**2 + (Y-Cy)**2)/(2*R)**2)
        Hi = 1 - Lo
    if Mode == "Step":
        first = (X-Cx)**2 + (Y-Cy)**2
        second = R**2
        Lo[first < second] = 1
        Hi = 1 - Lo

    J = A1 * Lo
    J1 = np.fft.ifftshift(J)
    B1 = np.fft.ifft2(J1)

    K = A1 * Hi
    K1 = np.fft.ifftshift(K)
    B2 = np.fft.ifft2(K1)

    low = np.abs(B1)
    high = np.abs(B2)

    return low, high