%% =============== NNMF =====================
function do_NNMF(datapar, datapath, resultsavedir, featdr_path)
% E:\New_Pattern_Unmixing\code\unmixing_functions\NNMF
disp('==============================  NNMF  =============================')
tic;
if count(py.sys.path,'E:\项目1：DULoc_experiments\HPA_large-scale_Unmixing\code\function\NNMF') == 0
    insert(py.sys.path,int32(0),'E:\项目1：DULoc_experiments\HPA_large-scale_Unmixing\code\function\NNMF');
end

import py.nnmf_py.*

nnmf_main(py.str(datapath),py.str(resultsavedir),py.str(featdr_path), py.str(datapar));
disp('Running Time of NNMF is ')
toc;
end