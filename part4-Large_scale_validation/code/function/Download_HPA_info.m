function Download_HPA_info(xmls_dir, SL_path, Selected_csv_path)
%DOWNLOAD_HPA_INFO downloading the xml as txt and extracting the infomation
% of selected images which we wanted
[Genelist,Genenamelist,Reliabilitylist,Mainlocationlist,...
    Addlocationlist] = readSLxlsx(SL_path);
HPAv20url='https://www.proteinatlas.org/';
protN = length(Genelist);
fid = fopen(Selected_csv_path, 'w'); % a
fwrite(fid,['Gene,Gene name,Reliability,Cell Line,Main,Addition,Img url' char(10)]);
for i=1:protN
    disp(i);
    GeneId = Genelist{i};
    Genename = Genenamelist{i};
    Reliability = Reliabilitylist{i};
    Mainloc = Mainlocationlist{i};
    Addiloc = Addlocationlist{i};
    geneurl = strcat(HPAv20url,GeneId,'.xml');
    disp(GeneId)
    %% download xml
    options = weboptions('Timeout',25);
    try
        sourcefile=webread(geneurl, options);
    catch ErrorInfo
        disp(ErrorInfo);
        continue;
    end
    save([xmls_dir '\' GeneId '.mat'],'sourcefile');
    ftxt = fopen([xmls_dir '\' GeneId '.mat'],'w');
    fwrite(ftxt,sourcefile);
    fclose(ftxt);
    
    %% extracting selected Images and type of cellLine
    % if Addition is '' -> continue
    if strcmp(Addiloc,'')
        continue
    end
    % extracting the 'selected part'
    [antibodyId, cellLineId, ImgUrl] = extract_SelectedInfo(sourcefile);
    % extracting selected cellLine
    cellLine = extract_CellLine(sourcefile, antibodyId, cellLineId);
    disp(cellLine)
    if strcmp(cellLine,'')
        continue
    end
    %% writing the infomation of images
    csvstr = [GeneId ',' Genename ',' Reliability ',' cellLine ',' Mainloc ',' Addiloc ',' ImgUrl char(10)];
    fwrite(fid,csvstr); 
end
fclose(fid);
end

