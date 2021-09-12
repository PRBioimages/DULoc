function S4_DataPacking
%S4_DATAPACKING Packing the data as the input of bestfitting
% 
%% Adding the paths
addpath(genpath('.\function'));
%% Packing multi-label data (selected images) and single-label data (base images)
select_csvdir = '..\Data\HPASelectedImg\CellLines_csvs';
base_csvdir = '..\Data\Base\CellLines_csvs';
Test_savedir = '..\Data\Test';
CellLines_matpath = '..\Results\CellLines_sorted.mat';
topnum = 3;
% PackingMultiLoc(select_csvdir,Test_savedir,CellLines_matpath,topnum);
PackingBaseLoc(base_csvdir,Test_savedir,CellLines_matpath,topnum)
end

