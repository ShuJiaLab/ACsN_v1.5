import numpy as np
import cupy as cp
from datetime import datetime
import os
from skimage import io

def ACSN_initialization(I, varargin=None):

    default = [[1], [90], 1, 0, "Slow", "ACSN_" + str(datetime.date(datetime.now())) + ".tif", "auto", 64, 0.25, "no", 0.15]

    Gain = np.array(default[0])
    Offset = np.array(default[1])
    Hotspot = default[2]
    Level = default[3]
    Mode = default[4]
    SaveFileName = default[5]
    Video = default[6]
    Window = default[7]
    alpha = default[8]
    QM = default[9]
    weight = default[10]

    if varargin != None:
        # Other stuff for initialization
        if "Gain" in varargin:
            Gain = varargin["Gain"]
        if "Offset" in varargin:
            Offset = varargin["Offset"]
        if "Hotspot" in varargin:
            Hotspot = varargin["Hotspot"]
        if "Level" in varargin:
            Level = varargin["Level"]
        if "Mode" in varargin:
            Mode = varargin["Mode"]
        if "SaveFileName" in varargin:
            SaveFileName = varargin["SaveFileName"]
        if "Video" in varargin:
            Video = varargin["Video"]
        if "Window" in varargin:
            Window = varargin["Window"]
            Window = max(32, Window)
            Window = min(256, Window)
        if "Alpha" in varargin:
            alpha = varargin["Alpha"]
            alpha = max(0.1, alpha)
        if "QualityMap" in varargin:
            QM = varargin["QualityMap"]
        if "Weight" in varargin:
            weight = varargin["Weight"]


    if (max(Offset.shape) == 1):
        Offset = Offset * np.ones(I[:, :, 0].shape)
    
    if (max(Gain.shape) == 1):
        Gain = Gain * np.ones(I[:, :, 0].shape)

    Gain[Gain < 1] = 1

    return I, Gain, Offset, Hotspot, Level, Mode, SaveFileName, Video, Window, alpha, QM, weight


