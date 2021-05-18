import numpy as np
from scipy.stats import pearsonr
# from HPA_multinomial_unmixing import point_squared


def point_squared(arr):
    return np.array([arr[i]**2 for i in range(len(arr))])


def MSE(pre_arr, true_arr):
    return np.sum(point_squared(pre_arr-true_arr))/len(pre_arr)


def PCCs(pre_arr, true_arr):
    return pearsonr(pre_arr, true_arr)[0]
