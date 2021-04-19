import numpy as np
from skimage import io
import math
import scipy
from bm3d import bm3d
from Gaussian_image_filtering import Gaussian_image_filtering
from scipy.optimize import curve_fit
import cupy as cp

def ACSN_core(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, w):
    
    R = 2 * NA / Lambda * PixelSize * I.shape[0]
    adj = 1.1
    R2 = (0.5 * I.shape[0] * adj)
    # multiplicative factor to adjust the sigma of the noie
    ratio = math.sqrt(R2/abs(R-R2))
    # rescaling
    I1 = (I - Offset)/Gain
    I1[I1 <= 0] = 1e-6
    I1[I1 > 10000] = 1e-6

    #Remove hotspots
    if (Hotspot == 1):
        
        # Fourier Filter
        R1 = min(R, len(I1)/2)
        
        _, high = Gaussian_image_filtering(I1, "Step", R1)
        
        # Median Filter
        I1b = np.lib.pad(I1, (2,2), 'edge') #I1b is still a cupy array after this line
        I_med = scipy.signal.medfilt2d(I1b)
        I_med = np.delete(I_med, [0, 1], 0)
        I_med = np.delete(I_med, [0, 1], 1)
        I_med = np.delete(I_med, [I_med.shape[0] - 2, I_med.shape[0] - 1], 0)
        I_med = np.delete(I_med, [I_med.shape[1] - 2, I_med.shape[1] - 1], 1)
        I1[abs(high) > abs(cp.mean(high) + 3 * cp.std(high))] = I_med[abs(high) > abs(cp.mean(high) + 3 * cp.std(high))]

        I1[I1 <= 0] = 1e-6


    #Fourier Filter 2
    R1 = min(R, len(I1)/2)

    _, high = Gaussian_image_filtering(I1, "Step", R1)

    #Evaluation of Sigma
    Values, t = np.histogram(high.flatten())
    BinCenters = t[:-1] + np.diff(t)/2
    bins = np.array(BinCenters)
    Values = np.array(Values)
    
    first_min = np.where(Values == min(Values))[0][0] #getting the index of the first min
    a1_est = bins[int(round(first_min/2))]
    a0_est = np.amax(Values) ##might need an axis

    def gaus(x,a0,a1):
        return a0*np.exp(-(1/2)*((x)/a1)**2)

    popt, _ = curve_fit(gaus, bins, Values, p0=[a0_est,a1_est])

    a = popt[1]

    sigma = w * ratio * a

    # normalization
    M1 = np.amax(I1)
    M2 = np.amin(I1)
    I2 = (I1 - M2)/(M1 - M2)

    # Denoising
    # scaling sigma for non-8 bit images
    if (M1 - M2) > 255:
        sigma = sigma/(M1 - M2) * 255

    #SPARSE FILTERING FUNCTION
    img = bm3d(I2, sigma) * (M1 - M2) + M2 # try exchanging the bm3d with the one in C; test the bm3d C version speed in isolation (<3.855 seconds)

    return img, sigma, I1