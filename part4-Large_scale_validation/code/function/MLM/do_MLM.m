%% =============== MLM =====================
function do_MLM(datapar, datapath, resultsavedir, featdr_path)
% introduction
disp('===============================  MLM  =============================')
tic;
load(datapath);
Base=BaseMat;
Mix=MixMat;
Frac=RateMat; 
if ~strcmp(featdr_path, '')
    load(featdr_path);
    Mix=MixMat_dr;
    Base=BaseMat_dr;
end
resultsavepath = [resultsavedir '\' datapar '_MLM.mat'];

F = Base';
X = Mix';
[N, L] = size(Mix);
threshold=1e-9; % The threshold to stop the algorithm
% The proposed algorithm for nonlinear unmixing based on MLM model

[P_MLM,MLM_coeff,M_est,MLM_obj]=MLMp(F,X,threshold);
MLM_R_tmp = corrcoef(MLM_coeff,Frac);
MLM_R = MLM_R_tmp(1,2);
MLM_MSE = sum(sum((MLM_coeff-Frac).^2))/N;
save(resultsavepath, 'MLM_coeff', 'MLM_R', 'MLM_MSE', 'P_MLM');
% save(resultsavepath, 'MLM_coeff', 'MLM_R', 'MLM_MSE');
disp('Running Time of MLM is ')
toc;
end