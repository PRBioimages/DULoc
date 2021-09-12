function S8_Estimation
%S8_ESTIMATION estimating the consistency between predicted fractions and
% HPA annotations
%% Adding path
addpath(genpath('./function'));
%% Initialization path and parameters
param = 'KMN';  % {'L','K','KM','KMN'}
CellLines = {'U-2 OS', 'A-431', 'U-251 MG'};
PatternNums = {'Double', 'Triple', 'Quatru', 'Pentu'};
rdir = '..\Results_prob_SP\';
switch param
    case 'L'
        result_dir = [rdir 'L-DULoc_Results'];
    case 'K'
        result_dir = [rdir 'K-DULoc_Results'];
    case 'M'
        result_dir = [rdir 'M-DULoc_Results'];
    case 'N'
        result_dir = [rdir 'N-DULoc_Results'];
    case 'KM'
        result_dir = [rdir 'KM-DULoc_Results'];
    case 'KMN'
        result_dir = [rdir 'KMN-DULoc_Results'];
end
All_Num_list = [];
Consists_list = [];
Correct_Num_list = [];
Misclass_Num_list = [];
for i=1:length(CellLines)
    Cell = CellLines{i};
    disp(Cell)
    Fract_dir = [result_dir '\' Cell '\Fraction'];
    OneHot_dir = [result_dir '\' Cell '\OneHot'];
    EstRes_dir = [result_dir '\' Cell];
    if ~exist(OneHot_dir,'dir')
       mkdir(OneHot_dir); 
    end
    EstRes_path = [EstRes_dir '\' Cell '_Estimation.mat'];
    
    All_img_ids = cell(length(PatternNums),1);
    Correct_img_ids = cell(length(PatternNums),1);
    Consists = [];
    All_Nums = [];
    Correct_Nums = [];
    Misclass_Num = [];
    for j=1:length(PatternNums)
        pattern = PatternNums{j};
        disp([pattern '---------------------------------------------------'])
        Fract_path = [Fract_dir '\' pattern '_Fraction.mat'];
        OneHot_path = [OneHot_dir '\' pattern '_OneHot.mat'];
        %% One-hot encoding
        [Img_id,pre_frac,true_Main,true_Addition] = Encoding_onehot(Fract_path, OneHot_path);
        %% Estimating accuracy
        [total_img, correct_img, consistency,N,n,sn] = Estimation(Img_id, pre_frac, true_Main, true_Addition);
        disp(['Total images number is ' num2str(N) ' and the correct images is ' num2str(n) '.'])
        disp(['The cosistency is ' num2str(consistency) '.'])
        %% Dividing the variables
        All_img_ids{i} = total_img;
        Correct_img_ids{i} = correct_img;
        Consists = [Consists; consistency];
        All_Nums = [All_Nums; N];
        Correct_Nums = [Correct_Nums; n];
        Misclass_Num = [Misclass_Num; sn];
        disp(sn)
%         switch pattern
%             case 'Double'
%                 Double_All = total_img;
%                 Double_Correct = correct_img;
%                 Double_Consist = consistency;
%                 Double_All_Num = N;
%                 Double_Correct_Num = n;
%             case 'Triple'
%                 Triple_All = total_img;
%                 Triple_Correct = correct_img;
%                 Triple_Consist = consistency;
%                 Triple_All_Num = N;
%                 Triple_Correct_Num = n;
%             case 'Quatru'
%                 Quatru_All = total_img;
%                 Quatru_Correct = correct_img;
%                 Quatru_Consist = consistency;
%                 Quatru_All_Num = N;
%                 Quatru_Correct_Num = n;
%             case 'Pentu'
%                 Pentu_All = total_img;
%                 Pentu_Correct = correct_img;
%                 Pentu_Consist = consistency;
%                 Pentu_All_Num = N;
%                 Pentu_Correct_Num = n;
%         end
    end
%     save(EstRes_path,...
%         'Double_All','Double_Correct','Double_Consist','Double_All_Num','Double_Correct_Num',...
%         'Triple_All','Triple_Correct','Triple_Consist','Triple_All_Num','Triple_Correct_Num',...
%         'Quatru_All','Quatru_Correct','Quatru_Consist','Quatru_All_Num','Quatru_Correct_Num',...
%         'Pentu_All','Pentu_Correct','Pentu_Consist','Pentu_All_Num','Pentu_Correct_Num');
    All_Num_list = [All_Num_list,All_Nums];
    Consists_list = [Consists_list,Consists];
    Correct_Num_list = [Correct_Num_list,Correct_Nums];
    Misclass_Num_list = [Misclass_Num_list,Misclass_Num];
    save(EstRes_path,'PatternNums','All_img_ids',...
        'Correct_img_ids','Consists','All_Nums','Correct_Nums');
end
save([result_dir '.mat'],'All_Num_list','Consists_list',...
    'Correct_Num_list', 'Misclass_Num_list');
end

