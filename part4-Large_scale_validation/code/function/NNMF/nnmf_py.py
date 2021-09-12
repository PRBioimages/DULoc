from nnmf_numpy import *
import scipy.io as sio
import os
from unmixing_estimation import *
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def run_nnmf_fun(mat_path):
    load_data = sio.loadmat(mat_path)

    mix_arr = load_data['MixSet']
    base_arr = load_data['BaseSet']

    base_size = np.shape(base_arr)[0]
    # X = np.transpose(mix_arr)
    basis, coeff, outlier, obj = robust_NMF(mix_arr.T, base_arr.T, base_size, 1, 'nndsvdar', 0.08, 1, 1e-9, 30000, 10000, None)
    exinds = coefficient_exchange(base_arr, mix_arr, coeff)
    pre_rate = coeff[exinds, :]
    # if isexchange == True:
    #     coeff[[0, 1], :] = coeff[[1, 0], :]
    # pre_rate = coeff
    return pre_rate


def coefficient_exchange(base_arr, mix_arr, raw_coeff):
    # isexchange = False
    rawT_coeff = raw_coeff.T
    basis = base_arr
###############################################################################
    se_list = []
    ind_list = []
    def permutation(perm_list, basis, begin, end):
        if begin == end:
            mix = np.dot(rawT_coeff, basis[perm_list, :])
            arr_se = np.sum(point_2d_squared(mix_arr - mix))
            se_list.append(arr_se)
            ind_list.append(perm_list)
        else:
            for i in range(begin, end):
                perm_list[i], perm_list[begin] = perm_list[begin], perm_list[i]
                permutation(perm_list, basis, begin + 1, end)
                perm_list[i], perm_list[begin] = perm_list[begin], perm_list[i]
    p_list = [i for i in range(base_arr.shape[0])]
    permutation(p_list, basis, 0, base_arr.shape[0])
###############################################################################
    ind_num = se_list.index(np.min(se_list))
    exinds = ind_list[ind_num]
    # basis1 = base_arr
    # basis2 = base_arr[[1, 0], :]
    #
    # mix1 = np.dot(rawT_coeff, basis1)
    # mix2 = np.dot(rawT_coeff, basis2)
    #
    # if np.sum(point_2d_squared(mix_arr-mix1)) >= np.sum(point_2d_squared(mix_arr-mix2)):
    #     isexchange = True
    # return isexchange
    return exinds


def point_2d_squared(arr_2d):
    squared_arr_2d = np.zeros(arr_2d.shape)
    for i in range(arr_2d.shape[0]):
        for j in range(arr_2d.shape[1]):
            squared_arr_2d[i][j] = arr_2d[i][j]**2
    return squared_arr_2d


def do_estimate(pre_rate, real_rate):
    pre_arr = np.array(pre_rate).flatten()
    # print(pre_arr.shape)
    real_arr = np.array(real_rate).flatten()
    mse = MSE(pre_arr, real_arr)
    r = PCCs(pre_arr, real_arr)
    return r, mse


def nnmf_main(mat_path, save_path):
    # save_path = os.path.join(save_dir, datapar + '_NNMF.mat')
    pre_rate = run_nnmf_fun(mat_path)
    sio.savemat(save_path, {'NNMF_coeff': pre_rate})


if '__main__' == __name__:
    mat_path = '..\\..\\NNMF_Temp\\temp_NNMF_Dataset2.mat'
    save_path = '..\\..\\NNMF_Temp\\temp_NNMF_save.mat'
    nnmf_main(mat_path, save_path)