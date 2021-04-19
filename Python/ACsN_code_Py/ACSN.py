import pickle
import os
import sys
import time
import numpy as np
from colorama import Fore, Back, Style

from ACSN_processing import ACSN_processing
from ACSN_initialization import ACSN_initialization
from ACSN_processing_parallel import ACSN_processing_parallel
from ACSN_processing_video import ACSN_processing_video
from numba import jit
import cupy as cp

# # varargin is a list with different datatypes
# # for python it will be a dictionary
# # varargin = {"Gain": xxx, "Offset": xxx, "Hotspot": xxx, "Level": xxx, 
#     # "Mode": xxx, "SaveFileName": xxx, 
#     # "Video": xxx, "Window": xxx, "Alpha": xxx, "QualityMap": xxx}

def ACSN(I,NA,Lambda,PixelSize,varargin):

    start = time.perf_counter()
    # Assumes I is a 3D variable
    Qscore = np.zeros((I.shape[2], 1))
    sigma = np.zeros((I.shape[2], 1))
    img = np.zeros(I.shape)
    Qmap = np.zeros(I.shape[0])
    I, Gain, Offset, Hotspot, Level, Mode, SaveFileName, Video, Window, alpha, QM, weight = ACSN_initialization(I, varargin=varargin)

    ## main theme

    if (Mode == "Fast"):
        img, Qmap, Qscore = ACSN_processing_parallel(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, QM, Qmap, Qscore, sigma, img, Video, weight)
    elif (Video == "yes"):
        img, Qmap, Qscore = ACSN_processing_video(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, QM, Qmap, Qscore, sigma, img, Video, weight)
    else:
        img, Qmap, Qscore = ACSN_processing(I, NA, Lambda, PixelSize, Gain, Offset, Hotspot, QM, Qmap, Qscore, sigma, img, weight)

    ## finale

    end = time.perf_counter()
    print("Elapsed Time: " + str(end - start) + " seconds" +"\n")
    print("Average Quality: ")
    Av_qI = np.mean(Qscore.flatten())
    if (Av_qI >= 0.6):
        print("High: " + str(Av_qI) + "\n")
    elif (abs(Av_qI - 0.5) < 0.1):
        print("Medium: " + str(Av_qI) + "\n")
    else:
        print("Low: " + str(Av_qI) + "\n")
    
    return Qscore, sigma, img, SaveFileName