import numpy as np
import scipy.io
import os
import pandas as pd


def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the ' + dirName + ' is created!---')
    else:
        print('---The dir is there!---')


if __name__ == '__main__':
    param = 'feat'  # 'feat'
    npy_file = ''
    if param == 'prob':
        npy_file = 'prob_test.npy'
    elif param == 'feat':
        npy_file = 'features_test.npy'

    test_list = ['Base', 'Double', 'Triple', 'Quatru', 'Pentu']
    Cell_list = ['U-2 OS', 'A-431', 'U-251 MG']
    raw_npy_dir = '..\\Results\\DeepFeatures\\bestfitting_npy'
    raw_mat_dir = '..\\Results\\DeepFeatures\\bestfitting_mat'

    for Cell in Cell_list:
        for test_name in test_list:
            npy_dir = os.path.join(raw_npy_dir, Cell, test_name, 'fold0')
            save_dir = os.path.join(raw_mat_dir, Cell, test_name)

            mkdir(save_dir)
            # get the size of Avgarr
            aug_list = os.listdir(npy_dir)
            exnpy = np.load(os.path.join(npy_dir, aug_list[0], npy_file))
            sumdata = np.zeros(exnpy.shape)

            # get npy in augment dir
            for aug_dir in aug_list:
                npy_path = os.path.join(npy_dir, aug_dir, npy_file)
                data = np.load(npy_path)

                sumdata = sumdata + data
                mat_path = os.path.join(save_dir, aug_dir+'.mat')
                print(mat_path)
                scipy.io.savemat(mat_path, {'bestfitting_data': data})

            Avgarr = sumdata/len(aug_list)
            avg_mat_path = os.path.join(raw_mat_dir, Cell, test_name + '_data.mat')
            scipy.io.savemat(avg_mat_path, {'bestfitting_data': Avgarr})