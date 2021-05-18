%% ===============khype (P) =====================
function [R, MSE, alpha_coeff] = do_Knonlinear(Mix,Base,Rate)
F = Base';
X = Mix';
[N, L] = size(Mix);
lambda = 100;
mu = 0.01;

tmp = pdist2(F,F);
par = 0; % Polynormial
sigma = par*max(tmp(:)); 
% sigma = 1;
[alpha_coeff, f_khype, K_Khype] = Knonlinear(sigma,lambda,mu,N,X,F);
R = corrcoef(alpha_coeff,Rate);
R = R(1,2);
MSE = mse(alpha_coeff-Rate);
% MSE = sum(sum((alpha_coeff-Rate).^2))/N;
% disp(MSE)
end