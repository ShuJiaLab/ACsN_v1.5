import numpy as np
from ACSN_core import ACSN_core
from joblib import Parallel, delayed
from Quality_Map import Quality_Map
from metric import metric
from im2tiles import im2tiles
from numba import jit
from bm3d import bm3d
from tiles2im import tiles2im
import vapoursynth as vs
from vapoursynth import core
import mvsfunc as mvf
import functools
from matplotlib import pyplot as plt

def ACSN_processing_video(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, QM, Qmap, Qscore, sigma, img, Video, weight, BM3DBackend, FourierAdj, HT, Step, verbose=True):
    if verbose:
        print("Doing video processing: ")

    I1 = np.zeros(I.shape)
    high = np.zeros(I.shape)
    sig = []

    for frame in range(0, I.shape[2]):
        img[:, :, frame], temp_sigma, I1[:, :, frame], high[:,:,frame] = ACSN_core(I[:, :, frame], NA, Lambda, PixelSize, Gain, Offset, Hotspot, weight,BM3DBackend, FourierAdj, HT, Step, verbose=verbose)
        sig.append(temp_sigma)

    Qscore = np.zeros((img.shape[2], 1))

    if (Video[0] != 'n') and (img.shape[2] > 1):
        if Video[0] != 'y':
            for i in range(0, img.shape[2]):
                Qscore[i] = metric(I1[:, :, i], img[:, :, i])
            if QM[0] == 'y':
                Qmap[:, :, i] = Quality_Map(img[:, :, i], I1[:, :, i])
    
        if (Qscore.mean(axis = 0) < 0.55) or (Video[0] == 'y'):

            print('Please wait... Additional 3D denoising required')

            # psd = sigma.mean(axis=0) * (0.6 - Qscore.mean(axis=0))

            # size_y = len(img[0])
            # size_x = len(img[1])
            # size_z = min(10, len(img[0][0]))
            # overlap = 0

            # Tiles = im2tiles(img, overlap, size_x, size_y, size_z)
            Tiles = img

            clip_placeholder = core.std.BlankClip(width = Tiles.shape[1], height = Tiles.shape[0], format= vs.GRAYS, length=Tiles.shape[2])

            def get_vsFrame(n, f, npArray):
                vsFrame = f.copy()
                np.copyto( np.asarray(vsFrame.get_write_array(0)), npArray[:, :, n] )
                return vsFrame

            clip = core.std.ModifyFrame(clip_placeholder, clip_placeholder, functools.partial(get_vsFrame, npArray=Tiles))
            flt = mvf.BM3D(clip, sigma=sig, profile1="np")

            Tiles = np.dstack([np.asarray(flt.get_frame(i).get_read_array(0))  for i in range(Tiles.shape[2])])
            
            img = Tiles
            #img = tiles2im(Tiles, overlap)

            for i in range(0, img.shape[2]):
                Qscore[i] = metric(I1[:, :, i], img[:, :, i])
                if QM[0] == 'y':
                    Qmap[:, :, i] = Quality_Map(I1[:, :, i], img[:, :, i])
        
    else:
        for i in range(0, img.shape[2]):
            Qscore[i] = metric(I1[:, :, i], img[:, :, i])
        if QM[0] == 'y':
            Qmap[:, :, i] = Quality_Map(I1[:, :, i], img[:, :, i])

    return img, Qmap, Qscore

