function [CellLines,CellNum] = Count_cellLines_hist(selected_img_csv)
%COUNT_CELLLINES_NUMBER 此处显示有关此函数的摘要
%   此处显示详细说明
[~,txt,~] = xlsread(selected_img_csv);
N=size(txt,1);
CellLines_list = txt(2:N,4);
CellrawLines = unique(CellLines_list);
CellrawNum = [];
for i=1:length(CellrawLines)
    CellLine = CellrawLines{i};
    num = length(find(strcmp(CellLines_list, CellLine)));
    CellrawNum = [CellrawNum, num];
end
[CellNum, CellInd] = sort(CellrawNum, 'descend');
CellLines=cell(1,length(CellrawLines));
for j=1:length(CellInd)
    CellLines{j} = CellrawLines{CellInd(j)};
end
end

