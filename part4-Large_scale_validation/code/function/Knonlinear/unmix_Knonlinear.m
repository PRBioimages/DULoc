%% ===============Knonlinear (plynomials) =====================
function [Knonlin_coeff] = unmix_Knonlinear(base,mix)
disp('====================   Knonlinear (plynomials) ====================')
tic
F = base';
X = mix';
[N, L] = size(mix);
lambda = 100;
mu = 0.01;

tmp = pdist2(F,F);
par = 0; % Polynormial
sigma = par*max(tmp(:)); 
% sigma = 1;
[Knonlin_coeff, f_Knonlin, K_Knonlin] = khype3(sigma,lambda,mu,N,X,F);
disp('Running Time of Knonlinear is ')
toc;
% disp(MSE)