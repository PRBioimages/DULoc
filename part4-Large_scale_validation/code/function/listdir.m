function [folder_list] = listdir(dir_name)
%LISTDIR 此处显示有关此函数的摘要
%   此处显示详细说明
flist=dir(dir_name);
folder_list = cell(1,length(flist)-2);
j=1;
for i=1:length(flist)
   if strcmp(flist(i).name,'.')==1||strcmp(flist(i).name,'..')==1||flist(i).isdir==0
       continue;
   end
   folder_list{j}= flist(i).name;
   j=j+1;
end
folder_list(cellfun(@isempty,folder_list))=[];
end

