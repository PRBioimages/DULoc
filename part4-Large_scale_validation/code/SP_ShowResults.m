function SP_ShowResults
%SP_SHOWRESULTS show the results about 1024-feat and 28-feat in different 
%   unmixing methods
%% addpaths
addpath('.\function\');
%% initial dataset paths and parameters
LABELS = {'Nucleoplasm', 'Nuclear membrane', 'Nucleoli', 'Nucleoli fibrillar center',...
    'Nuclear speckles', 'Nuclear bodies', 'Endoplasmic reticulum', 'Golgi apparatus',...
    'Peroxisomes', 'Endosomes', 'Lysosomes', 'Intermediate filaments', 'Actin filaments',...
    'Focal adhesion sites', 'Microtubules', 'Microtubule ends', 'Cytokinetic bridge',...
    'Mitotic spindle', 'Microtubule organizing center', 'Centrosome', 'Lipid droplets',...
    'Plasma membrane', 'Cell junctions', 'Mitochondria', 'Aggresome', 'Cytosol',...
    'Cytoplasmic bodies', 'Rods & rings'};

result_subdirs = {'..\Results_feat\L-DULoc_Results\','..\Results_prob\L-DULoc_Results\', ...
    '..\Results_feat\K-DULoc_Results\', '..\Results_prob\K-DULoc_Results\',...
    '..\Results_feat\M-DULoc_Results\', '..\Results_prob\M-DULoc_Results\',...
    '..\Results_feat\N-DULoc_Results\', '..\Results_prob\N-DULoc_Results\',...
    '..\Results_feat\KM2-DULoc_Results\', '..\Results_feat\KM4-DULoc_Results\',...
    '..\Results_prob\KM-DULoc_Results\', '..\Results_prob\KMN-DULoc_Results\'};

result_params = {'Methods', 'feat-L', 'prob-L', 'feat-K', 'prob-K', ...
     'feat-M', 'prob-M', 'feat-N', 'prob-N', 'feat-KM2', 'feat-KM4', ...
    'prob-KM', 'prob-KMN'}; 

CellLines_list = {'U-2 OS', 'A-431', 'U-251 MG'};  % 'U-2 OS', 'A-431', 'U-251 MG'
PatternNums_list = {'Double', 'Triple', 'Quatru'}; % 'Double', 'Triple', 'Quatru', 'Pentu'
for c = 1:length(CellLines_list)
    CellLines = CellLines_list{c};
    for p = 1:length(PatternNums_list) 
        PatternNums = PatternNums_list{p}; 
        images_dir = ['..\Data\HPASelectedImg\CellLines\' CellLines '\'];
        imgs_reault_dir = ['..\Image_results\' CellLines '\' PatternNums '\'];
        if ~exist(imgs_reault_dir, 'dir')
            mkdir(imgs_reault_dir)
        end
        load([result_subdirs{1} CellLines '\Fraction\' PatternNums '_Fraction.mat']);
        image_list = Img_id;
        for n = 1:length(image_list)
            image_path = [images_dir image_list{n}];
            blue_img = im2uint8(imread([image_path '_blue.jpg']).*0.3);
            green_img = imread([image_path '_green.jpg']);
            [r,c] = size(blue_img);
            zero_img = im2uint8(zeros(r,c,3));

            Maindata = {};
            Addidata = {};
            Maindata{1} = 'Main';
            Addidata{1} = 'Addition';
            for i = 1:length(result_subdirs) 
                result_subdir = result_subdirs{i};
                load([result_subdir CellLines '\Fraction\' PatternNums '_Fraction.mat']);
                load([result_subdir CellLines '\OneHot\' PatternNums '_OneHot.mat']);

                main_label = Main{n};
                addi_label = Addition{n};
                predict_fractions = pre_frac{n};
                %%% get main_fractions and additional_fractions
                main_fraction = {};
                main_lab = {};
                addi_fraction = {};
                addi_lab = {};
                for m = 1:length(main_label)
                    main_fraction{m} = num2str(round(predict_fractions(main_label(m)+1), 4));
                    main_lab{m} = LABELS{main_label(m)+1};
                end
                for a = 1:length(addi_label)
                    addi_fraction{a} = num2str(round(predict_fractions(addi_label(a)+1), 4));
                    addi_lab{a} = LABELS{addi_label(a)+1};
                end
                %%% uitdata
                main_frac = strjoin(main_fraction, ',');
                main_lab = strjoin(main_lab, ',');
                Maindata{i+1} = main_frac;
                addi_frac = strjoin(addi_fraction, ',');
                addi_lab = strjoin(addi_lab, ',');
                Addidata{i+1}= addi_frac;
            end

            %% show the fractions

            Mdata = strjoin(Maindata, char(10));
            Adata = strjoin(Addidata, char(10));
            % show image
            figure(1);
            set(figure(1), 'Position', [100,200,1000,380])
            subplot(1,2,1);
            image = zero_img;
            image(:,:,2) = green_img;
            image(:,:,3) = blue_img;
            imshow(image)
            title(['Main: ' main_lab char(10) 'Additional: ' addi_lab])
            % show table
            subplot(1,2,2);
            subplot('position', [0.5,0.3,0.4,0.8]);
            text(0,0.3,result_params);
            text(0.25,0.3,Mdata);
            text(0.65,0.3,Adata);
            axis off;
            saveas(gcf,[imgs_reault_dir image_list{n} '_prediction.jpg']);
        end
   end
end
end

