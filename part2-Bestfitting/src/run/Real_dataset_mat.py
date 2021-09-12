import numpy as np
import scipy.io
import os
import pandas as pd
from mixed_fundamental_vectors import *


def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the ' + dirName + ' is created!---')
    else:
        print('---The dir is there!---')


def get_rate(m_rate):
    m_rate = m_rate.split('_')
    Lyso_num = float(m_rate[0])
    Mito_num = float(m_rate[1])
    Lyso_rate = Lyso_num / (1e-9 + Lyso_num + Mito_num)
    Mito_rate = Mito_num / (1e-9 + Lyso_num + Mito_num)
    return Lyso_rate, Mito_rate


# def get_csvinfo(csv_path, prob_path):
#     csvinfo = pd.read_csv(csv_path)
#     prob_np = np.load(prob_path)
#     img_ids = csvinfo['Id'].values
#     img_labels = csvinfo['Target'].values
#     img_rates = csvinfo['m_rate'].values
#
#     A_num = 10  # 10:  "lysosomes"
#     B_num = 23  # 23:  "mitochondria"
#     A_inds, B_inds, mix_inds = index_separate(img_labels, A_num, B_num)
#
#     f_A = get_fundamental_pattern(prob_np, A_inds)
#     f_B = get_fundamental_pattern(prob_np, B_inds)
#     realLysorate = np.zeros(shape=(len(mix_inds), 1), dtype=np.float)
#     realMitorate = np.zeros(shape=(len(mix_inds), 1), dtype=np.float)
#     mixprobarr = np.zeros(shape=(len(mix_inds), prob_np.shape[1]))
#     i = 0
#     for mix_id in mix_inds:
#         # get mixed rate
#         mix_rate = img_rates[mix_id]
#         # print(mix_rate)
#         # if mix_rate == '0_0':
#         #     continue
#         Lyso_rate, Mito_rate = get_rate(mix_rate)
#         realLysorate[i] = Lyso_rate
#         realMitorate[i] = Mito_rate
#
#         # get mix prob array
#         mixprobarr[i, :] = prob_np[mix_id, :]
#         i = i + 1
#
#     return realLysorate.T, realMitorate.T, np.array([f_A]), np.array([f_B]), mixprobarr


def get_csvinfo2(csv_path, prob_path):
    csvinfo = pd.read_csv(csv_path)
    prob_np = np.load(prob_path)
    img_ids = csvinfo['Id'].values
    img_labels = csvinfo['Target'].values
    img_rates = csvinfo['m_rate'].values

    A_num = 10  # 10:  "lysosomes"
    B_num = 23  # 23:  "mitochondria"
    A_inds, B_inds, mix_inds = index_separate(img_labels, A_num, B_num)

    f_A = get_fundamental_pattern(prob_np, A_inds)
    f_B = get_fundamental_pattern(prob_np, B_inds)
    all_ids = mix_inds + A_inds + B_inds
    realLysorate = np.zeros(shape=(len(all_ids), 1), dtype=np.float)
    realMitorate = np.zeros(shape=(len(all_ids), 1), dtype=np.float)
    mixprobarr = np.zeros(shape=(len(all_ids), prob_np.shape[1]))
    i = 0

    for mix_id in all_ids:
        # get mixed rate
        mix_rate = img_rates[mix_id]
        # print(mix_rate)
        # if mix_rate == '0_0':
        #     continue
        Lyso_rate, Mito_rate = get_rate(mix_rate)
        realLysorate[i] = Lyso_rate
        realMitorate[i] = Mito_rate

        # get mix prob array
        mixprobarr[i, :] = prob_np[mix_id, :]
        i = i + 1

    return realLysorate.T, realMitorate.T, np.array([f_A]), np.array([f_B]), mixprobarr



if __name__ == '__main__':
    DATA_DIR = '/home/mqxue/bestfitting/HPA_imgs/Dataset'
    RESULT_DIR = '/home/mqxue/bestfitting/result/submissions'
    SAVE_DIR = '/home/mqxue/bestfitting/result/CNN_output'


    csv_path = os.path.join(DATA_DIR, 'MitoLyso.csv')
    npy_dir = os.path.join(RESULT_DIR, 'MitoLyso')

    for params in ['feat', 'prob']:
        # save_sub_dir = ''
        # npy_file = ''
        if params == 'feat':
            save_sub_dir = 'CNN_penult_feat'
            npy_file = 'prob_test.npy'
        else:
            save_sub_dir = 'CNN_last_feat'
            npy_file = 'prob_test.npy'

        save_dir = os.path.join(SAVE_DIR, save_sub_dir)
        mat_path = os.path.join(save_dir, 'real.mat')
        mkdir(save_dir)
        # get the size of Avgarr
        aug_list = os.listdir(npy_dir)
        exnpy = np.load(os.path.join(npy_dir, aug_list[0], npy_file))
        summix = np.zeros(exnpy.shape)
        sumbase = np.zeros((2, exnpy.shape[1]))
        Rate = np.zeros((exnpy.shape[0], 0))

        # test model with a aug_dir

        for aug_dir in aug_list:
            # 'prob_test.npy' for last features And 'features_test.npy' for penultimate features
            prob_path = os.path.join(npy_dir, aug_dir, npy_file)
            realLysorate, realMitorate, f_A, f_B, mixprobarr = get_csvinfo2(csv_path, prob_path)
            base = np.vstack((f_A, f_B))
            mix = mixprobarr
            rate = np.vstack((realLysorate, realMitorate))
            # print(base.shape)
            # print(mix.shape)
            # print(rate.shape)

            summix = summix + mix
            sumbase = sumbase + base
            Rate = rate
            # mat_path = os.path.join(save_dir, aug_dir+'.mat')
            # print(mat_path)
            # scipy.io.savemat(mat_path, {'base': base, 'mix': mix, 'rate': rate})
        MixMat = summix / len(aug_list)
        BaseMat = sumbase / len(aug_list)
        RateMat = Rate
        scipy.io.savemat(mat_path, {'MixMat': MixMat, 'BaseMat': BaseMat, 'RateMat': RateMat})



