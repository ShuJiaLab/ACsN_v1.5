import numpy as np
import multiprocessing
import skimage
from ACSN_core import ACSN_core
from Quality_Map import Quality_Map
from metric import metric
from im2tiles import im2tiles
from tiles2im import tiles2im
from numba import prange, njit
import vapoursynth as vs
from vapoursynth import core
import mvsfunc as mvf
import functools
from tqdm import tqdm
import multiprocessing
from multiprocessing import Pool


def ACSN_core_helper(args):
    img, sigma_temp, Qscore, high = ACSN_core(
        I = args["image"],
        NA = args["NA"],
        Lambda = args["Lambda"],
        PixelSize = args["PixelSize"],
        Gain = args["Gain"],
        Offset = args["Offset"],
        Hotspot = args["Hotspot"],
        w = args["weight"],
        verbose = args["verbose"],
        BM3DBackend = args["BM3DBackend"],
        FourierAdj = args["FourierAdj"],
        HT = args["HT"],
        Step = args["Step"]
    )        

    return {"image": img, "sigma": sigma_temp, "QScore": Qscore, "high": high}

def ACSN_processing_parallel(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, QM, Qmap, Qscore, sigma, img, Video, weight, BM3DBackend, FourierAdj, HT, Step, verbose=True):
    if verbose:
        print("ACSN parallel processing:")

    sig = []
    I1 = np.zeros(I.shape)
    high = np.zeros(I.shape)

    # prepare data for parallel processing
    input_args = [{
        "image": I[:,:,i],
        "NA": NA,
        "Lambda": Lambda,
        "PixelSize": PixelSize,
        "Gain": Gain,
        "Offset": Offset,
        "Hotspot": Hotspot,
        "weight": weight ,
        "verbose": verbose,
        "BM3DBackend": BM3DBackend,
        "FourierAdj": FourierAdj,
        "HT": HT,
        "Step": Step
    } for i in range(I.shape[2])]

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        results = list(tqdm(pool.imap(ACSN_core_helper, input_args), total=len(input_args), desc="ACSN Parallel"))

    for i, res in tqdm(enumerate(results), total=len(results), desc="Gathering results"):
        img[:,:,i] = res["image"]
        sig.append(res["sigma"])
        I1[:,:,i] = res["QScore"]
        high[:,:,i] = res["high"]

    Qscore = np.zeros((img.shape[2], 1))

    if (Video[0] != 'n') and (img.shape[2] > 1):
        if Video[0] != 'y':
            for i in prange(0, img.shape[2]):
                Qscore[i] = metric(I1[:, :, i], img[:, :, i])
            if QM[0] == 'y':
                Qmap[:, :, i] = Quality_Map(img[:, :, i], I1[:, :, i])
    
        if (Qscore.mean(axis = 0) < 0.55) or (Video[0] == 'y'):
            print('Please wait... Additional 3D denoising required')

            # psd = sigma.mean(axis=0) * (0.6 - Qscore.mean(axis=0))

            # size_y = img.shape[0]
            # size_x = img.shape[1] #see if this works
            # size_z = min(10, img.shape[2])
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

            # img = tiles2im(Tiles, overlap)
            
            for i in prange(0, img.shape[2]):
                Qscore[i] = metric(I1[:, :, i], img[:, :, i])
            if QM[0] == 'y':
                Qmap[:, :, i] = Quality_Map(I1[:, :, i], img[:, :, i])

    
    else:
        for i in prange(0, img.shape[2]):
            Qscore[i] = metric(I1[:, :, i], img[:, :, i])
        if QM[0] == 'y':
            Qmap[:, :, i] = Quality_Map(I1[:, :, i], img[:, :, i])
    
    return img, Qmap, Qscore
        

