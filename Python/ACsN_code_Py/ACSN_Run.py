# % SYNOPSIS:
# %   [img, Qscore,elapsedTime, sigma] = ACSN(I,NA,Lambda,PixelSize,PropertyName,PropertyValue)
# %
# % INPUTS:
# %   I
# %       Noisy image: variable name or file name (only .tif files)
# %   NA
# %       Numerical Aperture
# %   Lambda
# %       Wavelength of the emitter
# %   PixelSize
# %       Pixel size in the image plane in micron (Camera pixel size divided by the magnification)
# %
# %   Properties:
# %
# %       Gain
# %           gain map of the Camera
# %       Offset
# %           map of the Camera offset
# %       Video
# %           'yes' | 'no' | 'auto' (default)
# %       Hotspot    (hotspot removal)
# %           0 | 1 (default)
# %       Mode
# %           'Normal' | 'Fast' (default)
# %       Weight
# %           weight for noise estimation (decrease to reduce smoothing)
# %
# %
# % OUTPUTS:
# %   img
# %       Denoised image
# %   Qscore
# %       Image quality score
# %   sigma
# %       estimated noise variation
# %   elapsedTime
# %       elapsed time for the denoising

# varargin is a list with different datatypes
# for python it will be a dictionary
# varargin = {"Gain": xxx, "Offset": xxx, "Hotspot": xxx, "Level": xxx, 
    # "Mode": xxx, "SaveFileName": xxx, 
    # "Video": xxx, "Window": xxx, "Alpha": xxx, "QualityMap": xxx}

import pickle
import os
from skimage import io
import sys
import time
from pathlib import Path
import numpy as np
import cupy as cp
import pickle

from numpy import newaxis
from ACSN import ACSN
from scipy.io import loadmat
from matplotlib import pyplot as plt

path = Path(os.path.abspath(__file__))
code_dir = os.path.join(path.parent.absolute(),"..")
test_image_dir = os.path.join(path.parent.absolute(),"../Python Test Images/")

cmap = loadmat(os.path.join(test_image_dir,'cmap.mat'))['blow']
gain = loadmat(os.path.join(test_image_dir,'gain.mat'))['gain']
offset = loadmat(os.path.join(test_image_dir,'offset.mat'))['offset']

I = io.imread(os.path.join(test_image_dir,'TIRF_01_10ms.tif'))
color = False

I = I[0]

if color:
    if (I.ndim == 3):
        I = I
    else:
        I = np.array(I)[:, :, newaxis] # adding a third dimension

else:
    if (I.ndim == 3):
        I = np.transpose(I, (1, 2, 0)).copy() #transposing the first dimension to be the third dimension
    else:
        I = np.array(I)[:, :, newaxis] # adding a third dimension


I = I.astype(np.int16)

NA = 1.45
Lambda = .670
PixelSize = .065

varargin = {"Gain": gain, "Offset": offset, "Video": "no", "Weight": 0.2}
varargin = {"Weight": 0.2}

print("ACsN v1.5\n")

Qscore, sigma, img, SaveFileName = ACSN(I,NA,Lambda,PixelSize,varargin)

# Conversion to 16 bit array
img = img.astype(np.int16) # very low light - maybe use floating point to see the numbers after the comma; int conversion gets rid off info

# Show image
plt.imshow(I[:, :, 0], cmap="hot", interpolation="nearest")
plt.title("First Frame with No Correction")
# plt.show()

plt.imshow(img[:, :, 0], cmap="hot", interpolation="nearest")
plt.title("First Frame with Correction")
# plt.show()

img_save = np.transpose(img, (2, 0, 1)).copy()

directory_img = os.path.join(code_dir,"Python Image Results")

io.imsave(os.path.join(directory_img,SaveFileName), img_save)

# Save floating point matrix created from ACSN function - not transposed
directory_arr = os.path.join(code_dir,"Python Array Results")
pickle.dump(img, open(os.path.join(directory_arr,"floating_point_matrix_" + SaveFileName + ".pckl"), "wb" ) )
