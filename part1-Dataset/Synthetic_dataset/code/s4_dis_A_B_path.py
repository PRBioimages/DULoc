import os
import pandas as pd
import random

def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the '+dirName+' is created!---')
    else:
        print('---The dir is there!---')


combination = {1: ['cytosol', 'nucleoplasm'],
               2: ['cytosol', 'plasma membrane'],
               3: ['nucleoplasm', 'vesicles'],
               4: ['nucleoli', 'nucleoplasm'],
               5: ['mitochondria', 'nucleoplasm']}

def path_combination(labelA, labelB, img_csv, img_dir, txt_path):
    img_info = pd.read_csv(img_csv)
    samples = img_info['sample_id'].values
    labels = img_info['label'].values

    labelA_index = [i for i, label in enumerate(labels) if label == labelA]
    labelA_samples = [samples[ind] for ind in labelA_index]
    print('sampleA len = %d' % len(labelA_samples))

    labelB_index = [i for i, label in enumerate(labels) if label == labelB]
    labelB_samples = [samples[ind] for ind in labelB_index]
    print('sampleA len = %d' % len(labelB_samples))

    A_path = []
    for A_sample in labelA_samples:
        if not os.path.exists(os.path.join(img_dir, str(A_sample))):
            print('The A sample is missing!')
            continue
        cells = os.listdir(os.path.join(img_dir, str(A_sample)))
        for cell in cells:
            cell_path = os.path.join(img_dir, str(A_sample), cell)
            A_path.append(cell_path)

    B_path = []
    for B_sample in labelB_samples:
        if not os.path.exists(os.path.join(img_dir, str(B_sample))):
            print('The B sample is missing!')
            continue
        cells = os.listdir(os.path.join(img_dir, str(B_sample)))
        for cell in cells:
            cell_path = os.path.join(img_dir, str(B_sample), cell)
            B_path.append(cell_path)

    random.shuffle(A_path)
    random.shuffle(B_path)
    A_path_str = ','.join(A_path)
    B_path_str = ','.join(B_path)
    f = open(txt_path, 'a+')
    f.write(labelA + ',' + A_path_str + '\n')
    f.write(labelB + ',' + B_path_str + '\n')
    f.close()


if __name__ == '__main__':
        img_dir = 'new_transform'
        img_csv = 'final.csv'
        path_txts = 'path_txt'
        mkdir(path_txts)
        # match nucleus-mask and cell_mask between two cells
        for i in range(1, 6):
            labels = combination[i]
            print(labels, combination[i][0], combination[i][1])
            txt_save_path = os.path.join(path_txts, 'path_comb' + str(i) + '.txt')
            path_combination(combination[i][0], combination[i][1], img_csv, img_dir, txt_save_path)