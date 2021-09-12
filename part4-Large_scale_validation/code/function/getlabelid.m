function [labelnum,labelid,labelexist] = getlabelid(labelname)
%GETLABELID �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
LabelName = {'nucleoplasm','nuclear membrane','nucleoli',...
    'nucleoli fibrillar center','nuclear speckles','nuclear bodies',...
    'endoplasmic reticulum','golgi apparatus','peroxisomes',...
    'endosomes','lysosomes','intermediate filaments','actin filaments',...
    'focal adhesion sites','microtubules','microtubule ends',...
    'cytokinetic bridge','mitotic spindle','microtubule organizing center',...
    'centrosome','lipid droplets','plasma membrane','cell junctions',...
    'mitochondria','aggresome','cytosol','cytoplasmic bodies',...
    'rods & rings'};  % 'vesicles' would be add
labelexist=1;
labelid = [];
if strcmp(labelname, ' ')
    labelnum = 0;
else
    labels = strsplit(labelname,';');
    labelnum = size(labels,2);
    for i=1:labelnum
        ind = find(strcmp(LabelName,labels{i}));
%         ind = find(strcmp(LabelName,'vectory'));
        % if one of labelnames out of LabelName return labelexist=0
        if length(ind) == 0
            labelexist=0; 
            break;
        end
        labelid = [labelid ind-1];
    end
end
end

