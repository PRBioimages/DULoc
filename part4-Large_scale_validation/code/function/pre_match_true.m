function [pre2true] = pre_match_true(pre, true)
%PRE_MATCH_TRUE �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
true_label_num = size(true,1);
pre2=repmat(pre,true_label_num,1);
pre2true = sum((pre2 .* true),2);
end

