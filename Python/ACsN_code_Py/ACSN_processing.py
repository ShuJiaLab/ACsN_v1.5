import numpy as np
from skimage import io
from ACSN_core import ACSN_core
from Quality_Map import Quality_Map
from metric import metric

def ACSN_processing(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, QM, Qmap, Qscore, sigma, img, weight):
    print("Doing normal processing: ")

    I1 = np.zeros((I.shape))

    for i in range(0, I.shape[2]):
        img[:, :, i], sigma[i], I1[:, :, i] = ACSN_core(I[:, :, i], NA, Lambda, PixelSize, Gain, Offset, Hotspot, weight)
        if (QM[0] == "y"):
            Qmap[:, :, i] = Quality_Map(img[:, :, i], I1)
        
        Qscore[i] = metric(I1[:, :, i], img[:, :, i])

    return img, Qmap, Qscore