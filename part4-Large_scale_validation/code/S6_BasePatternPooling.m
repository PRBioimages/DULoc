function S6_BasePatternPooling
%S6_BASEPATTERNPOOLING getting the base patterns and conducting the average
% pooling operation

%% Adding path
addpath(genpath('.\function'));
%% Initializing path, loading data and corresponding labels
CellLines = {'U-2 OS', 'A-431', 'U-251 MG'};
topnum = 3;
BaseLabelMat = '..\Data\Test\mat';
BaseDataMat = '..\Results\DeepFeatures\bestfitting_feat_mat';
result_dir = '..\Results\BasePattern_feat';
if ~exist(result_dir,'dir')
   mkdir(result_dir); 
end
for i=1:topnum
    CellLine = CellLines{i};
    baselabelpath = [BaseLabelMat '\' CellLine '\Base.mat'];
    basedatapath = [BaseDataMat '\' CellLine '\Base_data.mat'];
    basesavepath = [result_dir '\' CellLine '_base.mat'];
    
    load(baselabelpath);
    Base_label = Label;
    load(basedatapath);
    Base_data = bestfitting_data;
    %% Generating Base pattern
    genBasePattern(basesavepath, Base_label, Base_data);
end
end

