function [alpha_coeff] = unmix_NNMF(BaseSet, MixSet)
%UNMIX_NNMF 此处显示有关此函数的摘要
%   此处显示详细说明
if count(py.sys.path,'E:\项目1：DULoc_experiments\HPA_large-scale_Unmixing\code\function\NNMF') == 0
    insert(py.sys.path,int32(0),'E:\项目1：DULoc_experiments\HPA_large-scale_Unmixing\code\function\NNMF');
end

if count(py.sys.path,'E:\项目1：DULoc_experiments\HPA_large-scale_Unmixing\code\function\NNMF') == 0
    insert(py.sys.path,int32(0),'E:\项目1：DULoc_experiments\HPA_large-scale_Unmixing\code\function\NNMF');
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
save(TempSet,'MixSet','BaseSet');
% NNMF unmixing
nnmf_main(py.str(TempSet),py.str(TempResult));
load(TempResult);
alpha_coeff = NNMF_coeff;
if exist(TempFolder,'dir')
    deletefiles(TempFolder); 
end
end

