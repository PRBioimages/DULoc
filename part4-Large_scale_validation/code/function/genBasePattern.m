function genBasePattern(base_path, single_label, single_data)
%GENBASEPATTERN 此处显示有关此函数的摘要
%   此处显示详细说明
Base = [];
Basesize = [];
for i=1:28
    labelname = i-1;
    sub_label_base = [];
%     sub_label_base = zeros(1,size(single_data,2));
    for j=1:length(single_label)
        if labelname==single_label{j}
            sub_label_base = [sub_label_base;single_data(j, :)];
        end
    end
    Basesize = [Basesize;size(sub_label_base,1)];
    if size(sub_label_base,1)==0
        sub_avg_base = zeros(1,size(single_data,2));
    else
        sub_avg_base = mean(sub_label_base);
    end
    Base = [Base;sub_avg_base];
end
save(base_path,'Base','Basesize');
end

