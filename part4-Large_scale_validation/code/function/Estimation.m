function [total_img,acc_img,acc,N,n,sn] = Estimation(...
    Img_ids, predicts, true_Mains, true_Additions)
%ESTIMATION 此处显示有关此函数的摘要
%   此处显示详细说明
total_img = cell(size(Img_ids));
acc_img = cell(size(Img_ids));
N = 0;
n = 0;
sn = 0;
for i=1:length(Img_ids)
    img = Img_ids{i};
    pre = predicts{i};
    pre = round(pre, 9);
    main = true_Mains{i};
    addi = true_Additions{i};
    
    pre2main = pre_match_true(pre, main);
    pre2addi = pre_match_true(pre, addi);
    N = N+1;
    total_img{N}=img;
% 1.skip the sample with lacked predicted annotation
%     pre_main_addi = [pre2main;pre2addi];
%     [~, ~, value] = find(pre_main_addi);
%     if size(value,1) < size(pre_main_addi,1)
%         sn = sn+1;
%         continue;
%     end
%         
% 2.skip the sample with single predicted annotation
%     sum_pre_main_addi = sum([pre2main;pre2addi],2);
%     if find(sum_pre_main_addi==1)
%         sn = sn+1;
%         continue;
%     end
% 
% 3.skip to the sample that pre not match main_true and addiction_true
%     if sum(sum(pre2main))==0||sum(sum(pre2addi))==0
%         sn = sn+1;
%         continue;
%     end

%     N = N+1;
%     total_img{N}=img;
    % if all elements in pre2main is higher than that in pre2addi
    if min(min(pre2main)) >= max(max(pre2addi))
        n = n+1;
        acc_img{N}=img;
    else
        acc_img{N}=[];
    end
end
% calculate acc
if N == 1
    acc = 0;
else
    acc = n/N;
end
tmp_total_img = total_img;
total_img(cellfun(@isempty,tmp_total_img))=[];
acc_img(cellfun(@isempty,tmp_total_img))=[];

end

