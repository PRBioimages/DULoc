function [isbase,base] = getBase(Base, labels)
%GETBASE selecting the Base according the labels
%   judging whether the Base is existing(sum == 0 -> no; sum != 0 -> yes)
base = [];
isbase = 1;
for i=1:length(labels)
    labelnum = labels(i)+1;
    sub_base = Base(labelnum, :);
    if sum(sub_base.*sub_base)==0
        isbase = 0;
        break;
    end
    base = [base;sub_base];
end
end

