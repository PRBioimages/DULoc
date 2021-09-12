function [cellLine] = extract_CellLine(sourcefile, antibodyId, cellLineId)
%EXTRACT_CELLLINE extracting the cellLine of the selected images according 
% initial
cellLine = '';
% cut the antybodies parts
ind1 = strfind(sourcefile,'</cellTypeExpression>');
ind2 = strfind(sourcefile,'</entry>');
CellAtlasInfo = sourcefile(ind1+length('</cellTypeExpression>')+1:ind2(1)-1);

antyind1L = strfind(CellAtlasInfo,'<antibody id=');
antyind2L = strfind(CellAtlasInfo,'</antibody>');
for i=1:length(antyind1L)
    antyind1 = antyind1L(i);
    antyind2 = antyind2L(i);
    antyInfo = CellAtlasInfo(antyind1-1:antyind2-1);
    
    % determine whather the anty is selected anty
    anind1 = strfind(antyInfo, '<antibody id="');
    anind2 = strfind(antyInfo, '" releaseVersion=');
    antybody = antyInfo(anind1+length('<antibody id="'):anind2-1);
    if size(strfind(antybody,antibodyId),1)==0
        continue;
    end
     % cuting the CellExpression part
    cellind1 = strfind(antyInfo, '<cellExpression source="HPA" technology="ICC/IF"');
    cellind2 = strfind(antyInfo, '</cellExpression>');
    CellExprInfo = antyInfo(cellind1:cellind2);

    % cuting the data part
    dataind1L = strfind(CellExprInfo, '<data>');
    dataind2L = strfind(CellExprInfo, '</data>');
    for j=1:length(dataind1L)
        dataind1 = dataind1L(j);
        dataind2 = dataind2L(j);
        dataInfo = CellExprInfo(dataind1:dataind2);

        % determine whether cellLineId corresponds to the data
        if size(strfind(dataInfo,[cellLineId '_']))==0
            continue;
        else
            % if yes, cuting the cellLine part
            cellind1 = strfind(dataInfo, '<cellLine organ=');
            cellind2 = strfind(dataInfo, '</cellLine>');
            cellline1 = dataInfo(cellind1:cellind2-1);

            cell2ind = strfind(cellline1, '>');
            cellLine = cellline1(cell2ind+1:length(cellline1));
            break;
        end
    end
end
end

