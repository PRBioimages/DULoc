function MasterSamples
%% Adding paths
addpath(genpath('.\functions'));
addpath(genpath('.\functions\Knonlinear'));
addpath(genpath('.\functions\Linear'));
addpath(genpath('.\functions\MLM'));
addpath(genpath('.\functions\RNNMF'));

%% Initialing
datapath = '.\Sampledata\CNN_last_feat\real.mat';
weightdir = '.\Sampledata\Weights';
savedir = '.\Sample_result\';
if ~exist(savedir, 'dir')
    mkdir(savedir)
end
method = 'N';  % L(linear), K(K-nonlinear), M(MLM), N(R-NNMF), K+M, K+M+N
param = 'last'; % penult,last
savepath = [savedir param '_' method '.mat'];
%% Prepocessing features
load(datapath);
[mix,base] = nonnegativity_of_matrix(MixMat,BaseMat);
rate = RateMat;
%% Methods
switch method
    case 'L'
        [R, MSE, fract] = do_Linear(mix,base,rate);
    case 'K'
        [R, MSE, fract] = do_Knonlinear(mix,base,rate);
    case 'M'
        [R, MSE, fract] = do_MLM(mix,base,rate);
    case 'N'
        [R, MSE, fract] = do_RNNMF(mix,base,rate);
    case 'K+M'
        [~, ~, Knonlin_coeff] = do_Knonlinear(mix,base,rate);
        [~, ~, MLM_coeff] = do_MLM(mix,base,rate);
        if strcmp(param, 'last')
            load([weightdir '\SynReal_prob_KM_Param.mat']);
        elseif strcmp(param, 'penult')
            load([weightdir '\SynReal_feat_KM_Param.mat']);
        else
            k_param2=0.5;
            M_param2=0.5;
        end
        fract = k_param2.*Knonlin_coeff + M_param2.*MLM_coeff;
        R = corrcoef(fract,rate);
        R = R(1,2);
        MSE = mse(fract-rate);
    case 'K+M+N'
        [~, ~, Knonlin_coeff] = do_Knonlinear(mix,base,rate);
        [~, ~, MLM_coeff] = do_MLM(mix,base,rate);
        [~, ~, RNNMF_coeff] = do_RNNMF(mix,base,rate);
        if strcmp(param, 'last')
            load([weightdir '\SynReal_prob_KMN_Param.mat']);
        elseif strcmp(param, 'penult')
            load([weightdir '\SynReal_feat_KMN_Param.mat']);
        else
            k_param2=0.33;
            M_param2=0.34;
            N_param2=0.33;
        end
        fract = k_param2.*Knonlin_coeff + M_param2.*MLM_coeff + N_param2.*RNNMF_coeff;
        R = corrcoef(fract,rate);
        R = R(1,2);
        MSE = mse(fract-rate);
end
save(savepath, 'fract', 'R', 'MSE');
end