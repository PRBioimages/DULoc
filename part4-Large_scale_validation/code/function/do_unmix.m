function [Fraction] = do_unmix(base, mix, param)
%DO_UNMIX unmixing the patterns according to param
%% processing the base and mix as non-negative
tmpMat = [mix;base];
tmpMatmin = min(min(tmpMat));
if tmpMatmin<0
    A = ones(size(mix))*abs(tmpMatmin);
    B = ones(size(base))*abs(tmpMatmin);
    mix = mix + A;
    base = base + B;
end
%% unmixing according to the method
switch param
    case 'L'
        % Linear unmixing
        L_Frac = gnf_lsqlin(base',mix');
        Fraction = L_Frac;
    case 'K'
        % K-nonlinear unmixing
        K_Frac = unmix_Knonlinear(base,mix);
        Fraction = K_Frac;
    case 'KM'
        % K-nonlinear + MLM
        parampath = '..\Data\Params_new\ProbSynReal_KM_Param.mat';
        load(parampath);      
        k_par = k_param2;
        M_par = M_param2;
%         k_par = 0;
%         M_par = 1;
        K_Frac = unmix_Knonlinear(base,mix);
        M_Frac = unmix_MLM(base,mix);
        Fraction = k_par.*K_Frac + M_par.*M_Frac;
    case 'KMN'
        % K-nonlinear + MLM + NNMF
%         parampath = '..\Data\Params_new\ProbSynReal_KMN_Param.mat';
%         load(parampath);
%         k_par = k_param2;
%         M_par = M_param2;
%         N_par = N_param2;
        N_Frac = unmix_NNMF(base,mix);
        Fraction = N_Frac;
%         K_Frac = unmix_Knonlinear(base,mix);
%         M_Frac = unmix_MLM(base,mix);
%         
%         Fraction = k_par.*K_Frac + M_par.*M_Frac + N_par.*N_Frac;
end

end

