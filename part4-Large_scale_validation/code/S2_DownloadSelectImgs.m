function S2_DownloadSelectImgs
%S2_DOWNLOADSELECTIMGS download the selected images and classify by
% checking '..\Result\CellLines_sorted.mat'
%% Addpath
addpath(genpath('./function'));
%% Downloading the Selected images in different cellLines
SelectedImg_dir = '..\Data\HPASelectedImg';
CellLine_dir = [SelectedImg_dir '\CellLines'];
CellLines_csvs_dir = [SelectedImg_dir '\CellLines_csvs'];
if ~exist(CellLine_dir,'dir')
   mkdir(CellLine_dir); 
end
if ~exist(CellLines_csvs_dir,'dir')
   mkdir(CellLines_csvs_dir); 
end
CellLines_matpath = '..\Results\CellLines_sorted.mat';
selected_csvpath = '..\Data\HPAInfo\selected_imgs.csv';
Download_CellLines_Img(CellLine_dir, CellLines_csvs_dir, ...
    CellLines_matpath, selected_csvpath);
end

