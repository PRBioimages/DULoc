%% =============== MLMp =====================
function [R, MSE, alpha_coeff] = do_MLM(Mix,Base,Rate)
    F = Base';
    X = Mix';
    [N, L] = size(Mix);
    threshold=1e-9; % The threshold to stop the algorithm
    % The proposed algorithm for nonlinear unmixing based on MLM model
%     tic;
    [P_MLMp,alpha_coeff,M_est,MLMp_obj]=MLMp(F,X,threshold);
%     toc;

    R = corrcoef(alpha_coeff,Rate);
    R = R(1,2);
%     MSE = sum(sum((alpha_coeff-Rate).^2))/N;
    MSE = mse(alpha_coeff-Rate);
%     disp(MSE)
end