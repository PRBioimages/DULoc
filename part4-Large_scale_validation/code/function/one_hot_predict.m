function [pre_mat] = one_hot_predict(label, frac)
%UNTITLED �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
class_num = 28;
pre_mat = zeros(1,class_num);
for i=1:size(label,2)
    pre_mat(1,label(i)+1)=frac(i);
end
end

