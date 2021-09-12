%% ===============Knonlinear (plynomials) =====================
function do_Knonlinear(datapar, datapath, resultsavedir, featdr_path)
disp('====================   Knonlinear (plynomials) ====================')
tic;
load(datapath)
Base=BaseMat;
Mix=MixMat;
Frac=RateMat; 
if ~strcmp(featdr_path, '')
    load(featdr_path);
    Mix=MixMat_dr;
    Base=BaseMat_dr;
end
resultsavepath = [resultsavedir '\' datapar '_Knonlinear.mat'];

F = Base';
X = Mix';
[N, L] = size(Mix);
lambda = 100;
mu = 0.01;

tmp = pdist2(F,F);
par = 0; % Polynormial
sigma = par*max(tmp(:)); 
% sigma = 1;
[Knonlin_coeff, f_Knonlin, K_Knonlin] = khype3(sigma,lambda,mu,N,X,F);
Knonlin_R_tmp = corrcoef(Knonlin_coeff,Frac);
Knonlin_R = Knonlin_R_tmp(1,2);
Knonlin_MSE = sum(sum((Knonlin_coeff-Frac).^2))/N;
save(resultsavepath, 'Knonlin_coeff', 'Knonlin_R', 'Knonlin_MSE', 'K_Knonlin', 'f_Knonlin');
disp('Running Time of Knonlinear is ')
toc;
% disp(MSE)