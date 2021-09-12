function [Genelist,Genenamelist,Reliabilitylist,Mainlocationlist,...
    Addlocationlist] = readSLxlsx(protein_info_xlsx)
%READPROTEINXLSX get the infomation from subcellular_location.xlsx
%   此处显示详细说明
[~,txt,~] = xlsread(protein_info_xlsx,'subcellular_location');
N=size(txt,1);
Genelist = txt(2:N,1);
Genenamelist = txt(2:N,2);
Reliabilitylist = txt(2:N,3);
Mainlocationlist = txt(2:N,4);
Addlocationlist = txt(2:N,5);
end

