function [true_mat] = one_hot_true(label)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
class_num = 28;
N=size(label,2);
if N==0
    true_mat = zeros(1,class_num);
else
    true_mat = zeros(N,class_num);
    for i=1:N
        true_mat(i,label(i)+1)=1;
    end
end
end

