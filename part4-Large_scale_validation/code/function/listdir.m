function [folder_list] = listdir(dir_name)
%LISTDIR �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
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

