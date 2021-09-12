function Download_CellLine_Base(Cmatpath, Gmatspath, Img_dir, csv_dir, topnum)
%DOWNLOAD_CELLLINE_BASE 
% load the data and path list
load(Cmatpath);
genes_list1 = dir(Gmatspath);
genes_list = cell(length(genes_list1)-2);
n=1;
for x=1:length(genes_list1)
    if strcmp(genes_list1(x).name,'.')||strcmp(genes_list1(x).name,'..')
        continue;
    end
    genes_list{n} = genes_list1(x).name;
    n=n+1;
end

for i=3:topnum
    CellLine = CellLines{i};
    BaseImgdir = [Img_dir '\' CellLine];
    if ~exist(BaseImgdir,'dir')
       mkdir(BaseImgdir); 
    end
    BaseCsvdir = [csv_dir '\' CellLine '.csv'];
    fid = fopen(BaseCsvdir, 'a'); % a
%     fwrite(fid,['Img_id,Gene,Cell Line,Reliability,Location' char(10)]);
    for j=6842:length(genes_list)
        disp([num2str(j) ':' genes_list{j}])
        genepath = [Gmatspath '\' genes_list{j}];
        load(genepath);
        ind1 = strfind(sourcefile,'</cellTypeExpression>');
        ind2 = strfind(sourcefile,'</entry>');
        CellAtlasInfo = sourcefile(ind1+length('</cellTypeExpression>')+1:ind2(1)-1);
        
        antyind1L = strfind(CellAtlasInfo,'<antibody id=');
        antyind2L = strfind(CellAtlasInfo,'</antibody>');
        for k=1:length(antyind1L)
            antyind1 = antyind1L(k);
            antyind2 = antyind2L(k);
            antyInfo = CellAtlasInfo(antyind1-1:antyind2-1);

            % cuting the CellExpression part
            localind1 = strfind(antyInfo, '<cellExpression source="HPA" technology="ICC/IF"');
            localind2 = strfind(antyInfo, '</cellExpression>');
            if size(localind1,1)==0
                continue;
            end
            CellExprInfo = antyInfo(localind1:localind2);
            
            % obtaining reliablity
            relyind1 = strfind(CellExprInfo,'<verification type="validation">');
            relyind2 = strfind(CellExprInfo,'</verification>');
            reliability = CellExprInfo(relyind1+length('<verification type="validation">'):relyind2-1);
            if strcmp(reliability,'approved')||strcmp(reliability,'uncertain')
                continue;
            end
            % cuting the data part
            dataind1L = strfind(CellExprInfo, '<data>');
            dataind2L = strfind(CellExprInfo, '</data>');
            for l=1:length(dataind1L)
                dataind1 = dataind1L(l);
                dataind2 = dataind2L(l);
                dataInfo = CellExprInfo(dataind1:dataind2);

                % determine whether cellLineId corresponds to the data
                if size(strfind(dataInfo,CellLine),1)==0
                    continue;
                else
                    %% choosing single location samples
                    % if yes, cuting the location
                    localind1 = strfind(dataInfo, '<location');
                    localind2 = strfind(dataInfo, '</location>');
                    % wether the single label
                    if size(localind1,2)==0||size(localind1,2)>1
                        continue;
                    end
                    location1 = dataInfo(localind1:localind2-1);
                    % wether the 'singleCellVariation'
                    if size(strfind(location1,'singleCellVariation'),2)
                        continue;
                    end
                    % geting the location
                    local2ind = strfind(location1, '>');
                    location = location1(local2ind+1:length(location1));
                    if strcmp(location,'vesicles')
                        continue;
                    end
                    %% downloading imgs
                    imgind1 = strfind(dataInfo,'<imageUrl>');
                    imgind2 = strfind(dataInfo,'</imageUrl>');
                    for m=1:size(imgind1,2)
                        disp(location)
                        imgUrl = dataInfo(imgind1(m)+length('<imageUrl>'):imgind2(m)-1);
                        [Img_id,isload] = download_images(imgUrl,BaseImgdir,'blue_red_green');
                        if isload
                            % construct csvstr
                            Gene = strrep(genes_list{j},'.mat','');
                            Reliability = reliability;
                            Location = location;
                            % write the csvstr into csv
                            csvstr = [Img_id ',' Gene ',' CellLine ',' Reliability ',' Location char(10)];
                            fwrite(fid,csvstr);
                        end
                    end
                end
            end
        end
    end
    fclose(fid);
end
end

