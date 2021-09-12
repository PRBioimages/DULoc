function Download_CellLines_Img(img_dir, csv_dir, matpath, csvpath)
%UNTITLED download the selected CellLine images and classify them 
%% load the information in mat and csv
load(matpath); % get CellLines
[~,txt,~] = xlsread(csvpath);
N=size(txt,1);
Genelist = txt(2:N,1);
Genenamelist = txt(2:N,2);
Reliabilitylist = txt(2:N,3);
CellLinelist = txt(2:N,4);
Mainlocationlist = txt(2:N,5);
Addlocationlist = txt(2:N,6);
Urllist = txt(2:N,7);
%% Download imgs
for i=12:length(CellLines)
    cellLine = CellLines{i};
    disp(cellLine)
    % create the img_save_path and csv_path
    img_save_dir = [img_dir '\' cellLine];
    csv_path = [csv_dir '\' cellLine '.csv'];
    if ~exist(img_save_dir,'dir')
        mkdir(img_save_dir);
    end
    fid = fopen(csv_path, 'w'); % a
    fwrite(fid,['Img_Id,Gene,Gene name,Reliability,Cell Line,Location,Main,Addition' char(10)]);
    for j=1:(N-1)
        disp(j)
        if ~strcmp(cellLine,CellLinelist{j})
            continue;
        end
        % cellLine == CellLinelist{j} download images
        ImgUrl = Urllist{j};
        [Img_id,isload] = download_images(ImgUrl,img_save_dir,'selected');
        if isload
            % construct csvstr
            Gene = Genelist{j};
            Genename = Genenamelist{j};
            Reliability = lower(Reliabilitylist{j});
            CellLine = cellLine;
            Main = lower(Mainlocationlist{j});
            Addition = lower(Addlocationlist{j});
            Location = [Main ';' Addition];
            % write the csvstr into csv
            csvstr = [Img_id ',' Gene ',' Genename ',' Reliability ',' CellLine ',' Location ',' Main ',' Addition char(10)];
            fwrite(fid,csvstr);
        end
    end
    fclose(fid);
end
end

