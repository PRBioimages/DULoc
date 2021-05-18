%% =============== NNMF =====================
function [R, MSE, alpha_coeff] = do_RNNMF(MixSet,BaseSet,RateSet)
% E:\New_Pattern_Unmixing\code\unmixing_functions\NNMF
% disp('==============================  NNMF  =============================')
% tic;
% if count(py.sys.path,'D:\Temp_EDisk\DULoc_codes\part3-Unmixing_methods\functions\RNNMF') == 0
%     insert(py.sys.path,int32(0),'D:\Temp_EDisk\DULoc_codes\part3-Unmixing_methods\functions\RNNMF');
% end

if count(py.sys.path,'.\function\RNNMF') == 0
    insert(py.sys.path,int32(0),'.\function\RNNMF');
end
TempFolder = 'NNMF_Temp';
if ~exist(TempFolder,'dir')
    mkdir(TempFolder)
end
import py.nnmf_py.*
TempSet = [TempFolder '\temp_NNMF_Dataset.mat'];
TempResult = [TempFolder '\temp_NNMF_Result.mat'];
if exist(TempSet,'file')||exist(TempResult,'file')
    TempSet = [TempFolder '\temp_NNMF_Dataset2.mat'];
    TempResult = [TempFolder '\temp_NNMF_Result2.mat'];
end
save(TempSet,'MixSet','BaseSet','RateSet');
% NNMF unmixing
nnmf_main(py.str(TempSet),py.str(TempResult));
load(TempResult);
R = NNMF_R;
MSE = NNMF_MSE;
alpha_coeff = NNMF_coeff;
if exist(TempFolder,'dir')
    deletefiles(TempFolder);
    
end

end