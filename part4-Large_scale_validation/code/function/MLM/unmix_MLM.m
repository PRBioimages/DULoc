%% =============== MLM =====================
function [MLM_coeff] = unmix_MLM(base,mix)
% introduction
disp('===============================  MLM  =============================')
tic;
F = base';
X = mix';
[N, L] = size(mix);
threshold=1e-9; % The threshold to stop the algorithm
% The proposed algorithm for nonlinear unmixing based on MLM model
[P_MLM,MLM_coeff,M_est,MLM_obj]=MLMp(F,X,threshold);
disp('Running Time of MLM is ')
toc;
end