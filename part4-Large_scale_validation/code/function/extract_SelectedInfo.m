function [antibodyId, cellLineId, ImgUrl] = extract_SelectedInfo(sourcefile)
%EXTRACT_SELECTEDINFO extracting the information of selected images
ind1 = strfind(sourcefile,'<cellExpression source="HPA" technology="ICC/IF">');
ind2 = strfind(sourcefile,'</cellExpression>');
if size(ind1)==0
    antibodyId = '';
    cellLineId = '';
    ImgUrl = '';
else
    protInfo = sourcefile(ind1+length('<cellExpression source="HPA" technology="ICC/IF">'):ind2(1)-1);
    imgurlind1 = strfind(protInfo,'<imageUrl>');
    imgurlind2 = strfind(protInfo,'</imageUrl>');
    ImgUrl = protInfo(imgurlind1+length('<imageUrl>'):imgurlind2(1)-1);
    
    imgurl_split = strsplit(ImgUrl, '/');
    antibodyId = imgurl_split{length(imgurl_split)-1};
    cellLineId = strtok(imgurl_split{length(imgurl_split)},'_');
end

end

