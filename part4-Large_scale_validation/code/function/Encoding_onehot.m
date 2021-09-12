function [Img_id,pre_frac,true_Main,true_Addition] = Encoding_onehot(Frac_result_path, onehot_save_path)
%ENCODING_ONEHOT 
load(Frac_result_path);
pre_frac = cell(size(Img_id));
true_Main = cell(size(Img_id));
true_Addition = cell(size(Img_id));

for i=1:length(Img_id)
    sub_pre = one_hot_predict(Label{i},Fraction{i});
    pre_frac{i} = sub_pre;
    
    sub_true_Main = one_hot_true(Main{i});
    true_Main{i} = sub_true_Main;
    
    sub_true_Addition = one_hot_true(Addition{i});
    true_Addition{i} = sub_true_Addition;
end
save(onehot_save_path, 'pre_frac', 'true_Main', 'true_Addition');
end

