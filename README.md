ACsN v1.5
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


## Python: ##
## System Requirements ##
### Hardware Requirements ###
ACsN requires a standard computer with enough RAM to support Python >= 3.7. For minimum performance, this will be a computer with about 2 GB of RAM. For optimal performance, we recomend the following specs:

RAM: 16+ GB; 
CPU: 6+ cores, 3.2+ GHz/core.

### Software Requirements ###
Python 3.7+
Windows OS 7+
Partial functionality on Mac OS

## Install ##
### Command Line ###
To run ACsN files:

 - Clone this repository
 - Run the command 'python setup.py install' after you're in the Sparse_Filtering folder
 - Install VapourSynth from https://github.com/vapoursynth/vapoursynth/releases
   - Install the R48 version if using Python 3.7. Otherwise, install the newest version
   - Once installed, got to the directory where vsrepo.py is located and install bm3d and msvfunc using the commands:
     - vsrepo.py install bm3d
     - vsrepo.py install msvfunc
 - Load your files using the ASCN_Run.py file. Run the ACSN_Run.py file in the terminal using the command (possible only when you're in the same directory):
   - python ACSN_Run.py

## Creators ##
Suraj Rajendran and Biagio Mandracchia

## MATLAB: ##
## System Requirements ##
### Hardware Requirements ###
ACsN requires a standard computer with enough RAM to support MATLAB 2018b. For minimum performance, this will be a computer with about 4 GB of RAM. For optimal performance, we recomend the following specs:

RAM: 16+ GB; 
CPU: 6+ cores, 3.2+ GHz/core.

### Software Requirements ###
MATLAB 2018b+ 

MATLAB "Curve Fitting" Toolbox

Windows OS 64 bit, Linux 64 bit or Mac OS X 64 bit*

## Install ##
### MATLAB Command Line ###
To run ACsN from MATLAB command line:

 - Add the folder ACsN_code to your MATLAB path (including subfolders).
 - In the command line type help ACSN or run the Sample code script in the Test Images folder to see the code usage.

### ImageJ/Fiji ###
To run ACsN from ImageJ/Fiji follow these steps:

 - Add the ImageJ-MATLAB update site to ImageJ. To see how, look at [here][ImageJ-MATLAB].
 - Go to Edit > Options > MATLAB and enter the file path for MATLAB licence.
 - Add the ACsN_code folder and subfolders to the MATLAB path.
 - Copy the file 'ACsN_.m' to the folder '<ImageJ installation folder name>\plugins\Scripts\Process\'.
 - Select an open image in ImageJ and then press Process > ACsN from the menu toolbar. 
 - To test the program you can use the images provided in the Test Images folder. See the file Settings.txt for the aquisition parameters.
	
The installation on a recommended computer should take less than 3 seconds.


\* Mac OS is only partially supported

[ImageJ-MATLAB]: https://imagej.net/MATLAB_Scripting#Prerequisites
[Nature Communications]: https://www.nature.com/articles/s41467-019-13841-8
