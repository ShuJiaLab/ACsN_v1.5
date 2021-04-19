# %SSIM Implementation of the similarity comparision in SSIM
# %--------------------------------------------------------------------------
# % Input:    intensity image a and b; patch size w.
# % Output:   struction similarity StrSim. 
# %--------------------------------------------------------------------------
# % Details can be found in the authors' original paper: 
# % Z.Wang, A.Bovik, H.Sheikh and E.Simoncelli, "Image quality assessment: 
# % From error visibility to structural similarity," IEEE Transactions on 
# % Image Processing, vol. 13, no. 4, pp. 600-612, Apr. 2004.
# %--------------------------------------------------------------------------

import numpy as np
import pickle
from scipy import ndimage, misc
from scipy.signal import fftconvolve
import math
from numba import jit, njit, cuda
import cupy as cp

def SSIM(a, b):
    c = 2e-4
    w = 8
    h = np.full((w,w),1/w**2)

    mu1 = fftconvolve(np.rot90(h), a, mode='valid')
    mu2 = fftconvolve(np.rot90(h), b, mode='valid')
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = fftconvolve(np.rot90(h), (a*a), mode='valid') - mu1_sq
    sigma2_sq = fftconvolve(np.rot90(h), (b*b), mode='valid') - mu2_sq

    sigma12 = fftconvolve((a*b), np.rot90(h), mode='valid') - mu1_mu2
    StrSim = (sigma12 + c)/(np.sqrt(sigma1_sq * sigma2_sq) + c)

    return StrSim

