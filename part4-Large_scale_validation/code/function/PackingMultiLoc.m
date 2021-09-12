function PackingMultiLoc(select_csvdir,Test_savedir,CellLines_matpath,topnum)
%PACKINGMULTILOC packing the multi-label samples as input of bestfitting
%   
load(CellLines_matpath);
Csv = [Test_savedir '\csv'];
Mat = [Test_savedir '\mat'];
for i=1:topnum
    %% Initial
    CellLine = CellLines{i};
    csv_dir = [Csv '\' CellLine];
    mat_dir = [Mat '\' CellLine];
    if ~exist(csv_dir,'dir')
       mkdir(csv_dir);
    end
    if ~exist(mat_dir,'dir')
       mkdir(mat_dir); 
    end
    selectcsvpath = [select_csvdir '\' CellLine '.csv'];
    %% Load raw base.csv
    csv_data = importdata(selectcsvpath);
    for labelnum=2:5
       switch labelnum
           case 2
               csv_path = [csv_dir '\Double.csv'];
               mat_path = [mat_dir '\Double.mat'];
               packing_multi_label(csv_path,mat_path,labelnum,csv_data);
           case 3
               csv_path = [csv_dir '\Triple.csv'];
               mat_path = [mat_dir '\Triple.mat'];
               packing_multi_label(csv_path,mat_path,labelnum,csv_data);
           case 4
               csv_path = [csv_dir '\Quatru.csv'];
               mat_path = [mat_dir '\Quatru.mat'];
               packing_multi_label(csv_path,mat_path,labelnum,csv_data);
           case 5
               csv_path = [csv_dir '\Pentu.csv'];
               mat_path = [mat_dir '\Pentu.mat'];
               packing_multi_label(csv_path,mat_path,labelnum,csv_data);
       end
    end
end
end

