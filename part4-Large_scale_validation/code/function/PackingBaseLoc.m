function PackingBaseLoc(base_csvdir,Test_savedir,CellLines_matpath,topnum)
%PACKINGBASELOC packing the single-label samples as input of bestfitting
%  
load(CellLines_matpath);
Csv = [Test_savedir '\csv'];
Mat = [Test_savedir '\mat'];
labelnum = 1;
for i=3:topnum
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
    basecsvpath = [base_csvdir '\' CellLine '.csv'];
    %% Load raw base.csv
    csv_data = importdata(basecsvpath);
    csv_path = [csv_dir '\Base.csv'];
    mat_path = [mat_dir '\Base.mat'];
    
    Img_id = cell(1,size(csv_data,1));
    Label = cell(1,size(csv_data,1));

    fid = fopen(csv_path, 'w');
    fwrite(fid,['Id,Target' char(10)]);
    j=1;
    for k=2:size(csv_data,1)
       test_sample = strsplit(csv_data{k},',');
       id = test_sample{1};
       label = test_sample{5};

       [Lnum,Lid,islabel] = getlabelid(label);
       if ~islabel||~(Lnum == labelnum)
           continue
       end

       Img_id{j}=id;
       Label{j}=Lid;
       csvlabel = num2str(Lid);
       
       csvstr=[id ',' csvlabel char(10)];
       fwrite(fid,csvstr);
       j=j+1; 
    end
    fclose(fid);
    Img_id2 = Img_id;
    Img_id(cellfun(@isempty,Img_id))=[];
    Label(cellfun(@isempty,Img_id2))=[];
    save(mat_path,'Img_id','Label');
    
end




end

