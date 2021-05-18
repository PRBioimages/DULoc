%% ===============Linear (lsqlin) =====================
function [R, MSE, alpha_coeff] = do_Linear(Mix,Base,Rate)
[N,F]=size(Mix);
alpha_coeff=[];
for n=1:N
    mix = Mix(n,:);
    l_fra = gnf_lsqlin(Base',mix');
    alpha_coeff = [alpha_coeff,l_fra];
end
R = corrcoef(alpha_coeff,Rate);
R = R(1,2);
MSE = mse(alpha_coeff-Rate);
% MSE = sum(sum((alpha_coeff-Rate).^2))/N;
% disp(MSE)
end