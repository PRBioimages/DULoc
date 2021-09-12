function [pre2true] = pre_match_true(pre, true)
%PRE_MATCH_TRUE 此处显示有关此函数的摘要
%   此处显示详细说明
true_label_num = size(true,1);
pre2=repmat(pre,true_label_num,1);
pre2true = sum((pre2 .* true),2);
end

