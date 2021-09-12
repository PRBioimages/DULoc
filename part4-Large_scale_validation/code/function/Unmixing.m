function Unmixing(label_path, data_path, save_Frac_path, base_path, param)
%NONLINEARUNMIXING conducting pattern unmixing using multiple methods
% load labels, datas and bases
load(label_path); % get Label
load(data_path);  % get Data
load(base_path);  % get Base
Data = bestfitting_data;
%% Unmixing
Fraction = cell(size(Label));
for i=1:length(Img_id)
    labels = Label{i};
    [isbase,base] = getBase(Base, labels);
    if ~isbase
       Frac = [];
       Fraction{i} = Frac;
       continue
    end
    mix = Data(i, :);
    Frac = do_unmix(base, mix, param);
    Fraction{i} = Frac';
end
tmp_Frac = Fraction;
Fraction(cellfun(@isempty,tmp_Frac))=[];
Img_id(cellfun(@isempty,tmp_Frac))=[];
Label(cellfun(@isempty,tmp_Frac))=[];
Main(cellfun(@isempty,tmp_Frac))=[];
Addition(cellfun(@isempty,tmp_Frac))=[];
save(save_Frac_path,'Img_id','Label','Main','Addition','Fraction');
end

