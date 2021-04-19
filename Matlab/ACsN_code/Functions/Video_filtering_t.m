
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  This function has been adapted from the BM4D algorithm for attenuation
%  of Gaussian noise in volumetric data. This algorithm reproduces the
%  results from the articles: 
%
%  [1] M. Maggioni, V. Katkovnik, K. Egiazarian, A. Foi, "A Nonlocal
%      Transform-Domain Filter for Volumetric Data Denoising and
%      Reconstruction", IEEE Trans. Image Process., vol. 22, no. 1, 
%      pp. 119-133, January 2013.  doi:10.1109/TIP.2012.2210725
%
%  [2] M. Maggioni, A. Foi, "Nonlocal Transform-Domain Denoising of 
%      Volumetric Data With Groupwise Adaptive Variance Estimation", 
%      Proc. SPIE Electronic Imaging 2012, San Francisco, CA, USA, Jan. 2012.
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Copyright (c) 2010-2015 Tampere University of Technology.
% All rights reserved.
% This work should only be used for nonprofit purposes.
%
% AUTHOR:
%     Matteo Maggioni, email: matteo.maggioni _at_ tut.fi
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
