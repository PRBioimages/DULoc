from nnmf_numpy import *
import scipy.io as sio
import os
from unmixing_estimation import *
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def run_nnmf_fun(mat_path):
    load_data = sio.loadmat(mat_path)

    mix_arr = load_data['MixSet']
    base_arr = load_data['BaseSet']
    real_rate = load_data['RateSet']

    base_size = np.shape(base_arr)[0]
    X = np.transpose(mix_arr)
    basis, coeff, outlier, obj = robust_NMF(X, base_arr.T, base_size, 1, 'NMF', 0.08, 1, 1e-9, 20000, 10000, None)
    isexchange = coefficient_exchange(base_arr, mix_arr, coeff)
    if isexchange == True:
        coeff[[0, 1], :] = coeff[[1, 0], :]
    pre_rate = coeff
    return pre_rate, real_rate


def coefficient_exchange(base_arr, mix_arr, raw_coeff):
    isexchange = False
    rawT_coeff = raw_coeff.T
    basis1 = base_arr
    basis2 = base_arr[[1, 0], :]

    mix1 = np.dot(rawT_coeff, basis1)
    mix2 = np.dot(rawT_coeff, basis2)

    if np.sum(point_2d_squared(mix_arr-mix1)) >= np.sum(point_2d_squared(mix_arr-mix2)):
        isexchange = True
    return isexchange


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
    pre_rate, real_rate = run_nnmf_fun(mat_path)
    r, mse = do_estimate(pre_rate, real_rate)
    sio.savemat(save_path, {'NNMF_coeff': pre_rate, 'NNMF_R': r, 'NNMF_MSE': mse})

# def nnmf_test(mat_path, dr_path):
#     pre_rate, real_rate = run_nnmf_fun(mat_path, dr_path)
#     return pre_rate, real_rate


# if __name__ == '__main__':
#     mat_path = 'E:\\New_Pattern_Unmixing\\Dataset_bestfitting\\probabilities\\real.mat'
#     dr_path = ''
#     pre_rate, real_rate = nnmf_test(mat_path, dr_path)
#     r, mse = do_estimate(pre_rate, real_rate)
#     print('correlation coefficient: ' + str(r))
#     print('MSE: ' + str(mse))