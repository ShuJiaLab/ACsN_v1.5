import numpy as np
from skimage import io
from ACSN_core import ACSN_core
from Quality_Map import Quality_Map
from metric import metric
from tqdm import tqdm

def ACSN_processing(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, QM, Qmap, Qscore, sigma, img, weight, BM3DBackend, FourierAdj, HT, Step, verbose=True):
    if verbose:
        print("ACSN single processing: ")

    I1 = np.zeros((I.shape))
    high = np.zeros(I.shape)

    for i in tqdm(range(0, I.shape[2]),desc="ACSN Single"):
        img[:, :, i], sigma[i], I1[:, :, i], high[:,:,i] = ACSN_core(I[:, :, i], NA, Lambda, PixelSize, Gain, Offset, Hotspot, weight, BM3DBackend, FourierAdj, HT, Step, verbose=verbose)
        if (QM[0] == "y"):
            Qmap[:, :, i] = Quality_Map(img[:, :, i], I1)
        
        Qscore[i] = metric(I1[:, :, i], img[:, :, i])

    return img, Qmap, Qscore