function S3_DownloadBaseImgs
%S3_DOWNLOADBASEIMGS download the base images
%   
%% Addpath
addpath(genpath('./function'));
%% Downloading the Base images in different cellLines
Base_dir = '..\Data\Base';
Base_Img_dir = [Base_dir '\CellLines'];
Base_csv_dir = [Base_dir '\CellLines_csvs'];
if ~exist(Base_Img_dir,'dir')
   mkdir(Base_Img_dir); 
end
if ~exist(Base_csv_dir,'dir')
   mkdir(Base_csv_dir); 
end
CellLines_matpath = '..\Results\CellLines_sorted.mat';
Gene_matspath = '..\Data\HPAInfo\HPA_xmls';
topnum = 3;
Download_CellLine_Base(CellLines_matpath, Gene_matspath,...
    Base_Img_dir, Base_csv_dir, topnum);
end

