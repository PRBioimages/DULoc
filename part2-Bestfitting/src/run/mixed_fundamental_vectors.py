import numpy as np


def index_separate(img_labels, A_num, B_num):
    A_ind = []
    B_ind = []
    mix_ind = []
    for i in range(len(img_labels)):
        if img_labels[i] == str(A_num):
            A_ind.append(i)
        elif img_labels[i] == str(A_num) + ' ' + str(B_num):
            mix_ind.append(i)
        elif img_labels[i] == str(B_num):
            B_ind.append(i)

    return A_ind, B_ind, mix_ind


def get_fundamental_pattern(prob_np, index_list):
    new_prob_np = np.zeros(shape=(len(index_list), prob_np.shape[1]))
    i = 0
    for ind in index_list:
        new_prob_np[i, :] = prob_np[ind, :]
        i = i + 1
    # 计算每一列的均值
    f_vector = np.mean(new_prob_np, axis=0)
    return f_vector


def HPA_normalize(vector):
    v_sum = 1.e-9 + np.sum(vector)
    return vector / v_sum


def get_key(dict, value):
    return list(dict.keys())[list(dict.values()).index(value)]

