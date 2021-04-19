
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% This function has been adapted from the BM3D algorithm for attenuation of
% additive white Gaussian noise from grayscale images. This algorithm
% reproduces the results from the article: 
%
%  [1] K. Dabov, A. Foi, V. Katkovnik, and K. Egiazarian, "Image Denoising
%      by Sparse 3D Transform-Domain Collaborative Filtering,"
%      IEEE Transactions on Image Processing, vol. 16, no. 8, August, 2007.
%      preprint at http://www.cs.tut.fi/~foi/GCF-BM3D.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Copyright (c) 2006-2019 Tampere University.
% All rights reserved.
% This work (software, material, and documentation) shall only
% be used for nonprofit noncommercial purposes.
% Any unauthorized use of this work for commercial or for-profit purposes
% is prohibited.
%
% AUTHORS:
%     Y. Mäkinen, L. Azzari, K. Dabov, A. Foi
%     email: ymir.makinen@tuni.fi
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
