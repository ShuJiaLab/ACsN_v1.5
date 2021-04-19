import numpy as np
import skimage
from metric import metric
from nrm import nrm
from im2tiles import im2tiles
from numba import jit, njit

def Quality_Map(img, ref):
    blockSize = 32
    
    size_y = min(blockSize, img.shape[0])
    size_x = min(blockSize, img.shape[1])
    size_z = 1

    # Tiles_img = im2tiles(img, size_x, size_y, size_z)
    # Tiles_ref = im2tiles(ref, size_x, size_y, size_z)

    Tiles_img = img
    Tiles_ref = ref

    for idx in range(0, Tiles_img.size):
        n1 = metric(255 * nrm(Tiles_ref[idx]), 255 * nrm(Tiles_img[idx]))
        Tiles_img[idx] = n1 * np.ones(Tiles_img[idx].shape)
    
    Qmap = list(Tiles_img)

    return Qmap