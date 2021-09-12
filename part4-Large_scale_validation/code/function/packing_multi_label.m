function packing_multi_label(csv_path,mat_path,labelnum,test_data)
%PACKING_MULTI_LABEL 此处显示有关此函数的摘要
%   此处显示详细说明
Img_id = cell(1,size(test_data,1));
Rely_score = cell(1,size(test_data,1));
Label = cell(1,size(test_data,1));
Main = cell(1,size(test_data,1));
Addition = cell(1,size(test_data,1));

fid = fopen(csv_path, 'w');
fwrite(fid,['Id,Target' char(10)]);
j=1;
for i=2:size(test_data,1)
   test_sample = strsplit(test_data{i},',');
   id = test_sample{1};
   rely = test_sample{4};
   label = test_sample{6};
   main = test_sample{7};
   addition = test_sample{8};
   
   [Lnum,Lid,islabel] = getlabelid(label);
   [~,Mid,~] = getlabelid(main);
   [~,Aid,~] = getlabelid(addition);
   
   if ~islabel||~(Lnum == labelnum)
       continue
   end
   
   Img_id{j}=id;
   Rely_score{j} = rely;
   Label{j}=Lid;
   Main{j}=Mid;
   Addition{j}=Aid;
   
   csvlabel=[];
   for x=1:Lnum
       csvlabel = [csvlabel num2str(Lid(x)) ' '];
   end
   csvlabel2=strip(csvlabel,'right',' ');
   
   csvstr=[id ',' csvlabel2 char(10)];
   fwrite(fid,csvstr);
   j=j+1; 
end
fclose(fid);
Img_id2 = Img_id;
Img_id(cellfun(@isempty,Img_id))=[];
Rely_score(cellfun(@isempty,Img_id2))=[];
Label(cellfun(@isempty,Img_id2))=[];
Main(cellfun(@isempty,Img_id2))=[];
Addition(cellfun(@isempty,Img_id2))=[];
save(mat_path,'Img_id','Rely_score','Label','Main','Addition');

end

