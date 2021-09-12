function S7_PatternUnmixing
%S7_PATTERNUNMIXING unmixing the mixed patterns of different cellLines
% using various methods.
%% Initialization path
addpath(genpath('./function'));
addpath(genpath('./function/Knonlinear'));
addpath(genpath('./function/MLM'));
addpath(genpath('./function/Linear'));
addpath(genpath('./function/NNMF'));
%% Determine multi labels data path
parm = 'L';   % {'L', 'K', 'KM'}
result_dir = '..\Results_prob\';
switch parm
    case 'L'
        method_result = [result_dir 'L-DULoc_Results'];
    case 'K'
        method_result = [result_dir 'K-DULoc_Results'];
    case 'KM'
        method_result = [result_dir 'M-DULoc_Results3'];
    case 'KMN'
        method_result = [result_dir 'N-DULoc_Results'];
end
CellLines = {'U-2 OS', 'A-431', 'U-251 MG'};  % 'double', 'triple', 'quatru' 
PattNums = {'Triple', 'Double', 'Quatru', 'Pentu'};
Base_dir = '..\Results\BasePattern';
Label_dir = '..\Data\Test\mat';
Data_dir = '..\Results\DeepFeatures\bestfitting_prob_mat';
for i=1:length(CellLines)
    Cell = CellLines{i};
    disp(Cell)
    Base_path = [Base_dir '\' Cell '_base.mat'];
    for j=1:length(PattNums)
        PattNum = PattNums{j};
        disp(PattNum)
        Frac_dir = [method_result '\' Cell '\Fraction'];
        if ~exist(Frac_dir,'dir')
           mkdir(Frac_dir); 
        end
        Lable_path = [Label_dir '\' Cell '\' PattNum '.mat'];
        Data_path = [Data_dir '\' Cell '\' PattNum '_data.mat'];
        Frac_path = [Frac_dir '\' PattNum '_Fraction.mat'];
        %% Pattern unmixing
        Unmixing(Lable_path, Data_path, Frac_path, Base_path, parm);
    end
end
end

