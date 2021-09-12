function S1_DownloadInfo
%S1_DOWNLOADINFO download the infomation from xml.
%   1)extrating the infomation of selected images and be writed into csv.
%   2)cut the infomation of antibody and download as txt.

%% Adding path
addpath(genpath('./function'));
%% load HPA information and selected images infomation
Info_dir = '..\Data\HPAInfo';
SL_path = [Info_dir '\subcellular_location.xlsx'];
Selected_img_path = [Info_dir '\selected_imgs.csv'];
xmls_dir = [Info_dir '\HPA_xmls'];
if ~exist(xmls_dir,'dir')
   mkdir(xmls_dir); 
end
Download_HPA_info(xmls_dir, SL_path, Selected_img_path);

%% count the amount of different cellLines
result_dir = '..\Results';
mat_path = [result_dir '\CellLines_sorted.mat'];
if ~exist(result_dir,'dir')
   mkdir(result_dir); 
end
[CellLines,CellNum] = Count_cellLines_hist(Selected_img_path);
save(mat_path,'CellLines','CellNum')
end

