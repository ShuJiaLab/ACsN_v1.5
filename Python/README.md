ACsN v1.5 - Python
=====
<div> 
	<table frame=void rules=none>
		<tr>
			<td width="75%">
				<div style="width:650px;float:left" align="justify">
					ACsN (pronounced as <i>action</i>) stands for Automatic Correction of sCMOS-related Noise. It combines an accurate estimation of noise variation with sparse filtering to eliminate the most relevant noise sources in the images of a sCMOS sensor. This results in a drastic reduction of pixel-dependent noise in sCMOS images and an enhanced stability of denoising performance at a competitive computational speed.
				</div>
			</td>
			<td width="25%">
				<div style="width:150px;float:right;">
					<img src="Picture2.jpg" width=150 height=150>
				</div>
			</td>
		</tr>
	</table>	
	<!-- <div style="clear:both"></div>  -->
</div>

## Citation ##
Please, cite our paper on [Nature Communications].

Mandracchia, B., Hua, X., Guo, C. et al. Fast and accurate sCMOS noise correction for fluorescence microscopy. Nat Commun 11, 94 (2020) doi:10.1038/s41467-019-13841-8

## System Requirements ##
### Hardware Requirements ###
ACsN requires a standard computer with enough RAM to support Python >= 3.7. For minimum performance, this will be a computer with about 2 GB of RAM. For optimal performance, we recomend the following specs:

- RAM: 16+ GB; 
- CPU: 6+ cores, 3.2+ GHz/core.
- GPU: CUDA supporting devices (optional)

### Software Requirements ###
- Python 3.7+
- Windows OS 7+
- Partial functionality on Mac OS

## Install ##
### Command Line ###
To run ACsN files:

 - Clone this repository
 - Run the command `python setup.py install` after you're in the `Sparse_Filtering` folder
 - Install VapourSynth from https://github.com/vapoursynth/vapoursynth/releases
   - Install the R48 version if using Python 3.7. Otherwise, install the newest version
   - Once installed, got to the directory where vsrepo.py is located and install bm3d and msvfunc using the commands:
		```bash
		vsrepo.py install bm3d
		vsrepo.py install msvfunc
		```
 - Load your files using the `ASCN_Run.py` file. Run the `ACSN_Run.py` file in the terminal using the command (possible only when you're in the same directory):
	```bash
	python ACSN_Run.py
	```

### GPU Acceleration on Gain Calibration
CPU version of linear regression fitting is available in [./ACsN_Calibration_Py/Camera_Calibration.py](./ACsN_Calibration_Py/Camera_Calibration.py)

For GPU accelerated fitting you will need the extra dependency [Gpufit](https://github.com/gpufit/Gpufit). Check the calibration process in [./ACsN_Calibration_Py/Camera_Calibration_GPU.py](./ACsN_Calibration_Py/Camera_Calibration_GPU.py)

### GPU BM3D

## Creators ##
Suraj Rajendran (Python Version) and Biagio Mandracchia
