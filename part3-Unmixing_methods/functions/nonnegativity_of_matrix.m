function [MixMat_dr,BaseMat_dr] = nonnegativity_of_matrix(MixMat,BaseMat)
%NONNEGATIVITY_OF_MATRIX 此处显示有关此函数的摘要

FeatMat = MixMat;
BaseRaw = BaseMat;

% Positive all mat number
tmpMat = [FeatMat;BaseRaw];
tmpMatmin = min(min(tmpMat));
if tmpMatmin < 0
    % disp(tmpMatmin)
    A = ones(size(FeatMat))*abs(tmpMatmin);
    B = ones(size(BaseRaw))*abs(tmpMatmin);
    MixMat_dr = FeatMat + A;
    BaseMat_dr = BaseRaw + B;
else
    MixMat_dr = MixMat;
    BaseMat_dr = BaseMat;
end
end

