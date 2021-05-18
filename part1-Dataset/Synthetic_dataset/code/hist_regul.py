import os
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit


# 高斯函数计算
def f_gauss(x, a1, a2, a3, m1, m2, m3, s1, s2, s3, d1, d2, d3):
    return a1 * np.exp(-((x - m1) / s1) ** 2) + d1 + a2 * np.exp(-((x - m2) / s2) ** 2) + d2 + a3 * np.exp(
        -((x - m3) / s3) ** 2) + d3

def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the ' + dirName + ' is created!---')
    else:
        print('---The dir is there!---')

def gray_scale_stretching(A_yvals, B_yvals, A_g_img, B_g_img):
    # 若sign == ‘A’说明new_g_img是由A图变换而来，若sign == ‘B’说明new_g_img是由B图变换而来
    sign = ''
    Acut_ind = np.argwhere(A_yvals < 15)
    Bcut_ind = np.argwhere(B_yvals < 15)
    # if Acut_ind == np.array([]):
    # 筛选出灰度直方图中所有yvals值都大于15的情况，即Acut_ind或Bcut_ind为空的情况，将它们的截止值设为255
    if Acut_ind.size == 0:
        Acut_ind = np.array([[255, 0]])
        print('Acut_ind is miss  ')
    elif Bcut_ind.size == 0:
        Bcut_ind = np.array([[255, 0]])
        print('Bcut_ind is miss  ' )
    # print(Acut_ind, Bcut_ind)
    # 筛选出Acut_ind[0][0]或Bcut_ind[0][0]小于100的情况，并将他们设置为（灰度值）最先大于100的那个值
    if Acut_ind[0][0] < 100:
        ind = np.argwhere(Acut_ind > 100)
        Acut_ind[0][0] = Acut_ind[ind[0][0]][ind[0][1]]
    elif Bcut_ind[0][0] < 100:
        ind = np.argwhere(Bcut_ind > 100)
        Bcut_ind[0][0] = Bcut_ind[ind[0][0]][ind[0][1]]
    # ----------------------------------------------
    # 由于这里A图和B图的size相等，因此new_g_img的大小我们就选择A图的吧
    new_g_img = np.zeros(shape=A_g_img.shape, dtype=np.uint8)

    if Acut_ind[0][0] < Bcut_ind[0][0]:
        # B较大,A图灰度值拉伸
        trans_rate = Bcut_ind[0][0] / Acut_ind[0][0]
        # A图的每个灰度值×trans_rate并取整
        sign = 'A'
        for i in range(A_g_img.shape[0]):
            for j in range(A_g_img.shape[1]):
                new_g_img[i][j] = int(A_g_img[i][j] * trans_rate)
                if new_g_img[i][j] > 255:
                    new_g_img[i][j] = 255

    elif Acut_ind[0][0] > Bcut_ind[0][0]:
        # A较大,B图灰度值拉伸
        trans_rate = Acut_ind[0][0] / Bcut_ind[0][0]
        # A图的每个灰度值×trans_rate并取整
        sign = 'B'
        for i in range(B_g_img.shape[0]):
            for j in range(B_g_img.shape[1]):
                new_g_img[i][j] = int(B_g_img[i][j] * trans_rate)
                if new_g_img[i][j] > 255:
                    new_g_img[i][j] = 255

    elif Acut_ind[0][0] == Bcut_ind[0][0]:
        sign = 'B'
        new_g_img = B_g_img
    return new_g_img, sign


def gray_hist_regulation(A_g_img, B_g_img):
    sign = ''
    A_hist = cv2.calcHist([A_g_img], [0], None, [255], [1, 255])
    B_hist = cv2.calcHist([B_g_img], [0], None, [255], [1, 255])
    x = np.array(range(1, 256))

    A_y = np.reshape(A_hist, (-1, 255))[0]
    # 多项式拟合
    A_z = np.polyfit(x, A_y, 30)
    A_p = np.poly1d(A_z)
    A_yvals = A_p(x)
    A_peak = find_peaks(A_yvals, distance=25)
    A_yvals = np.reshape(A_yvals, (-1, 1))

    B_y = np.reshape(B_hist, (-1, 255))[0]
    # 多项式拟合
    B_z = np.polyfit(x, B_y, 30)
    B_p = np.poly1d(B_z)
    B_yvals = B_p(x)

    B_peak = find_peaks(B_yvals, distance=25)
    B_yvals = np.reshape(B_yvals, (-1, 1))

    A_peak_list = []
    for ii in range(len(A_peak[0])):
        if A_yvals[A_peak[0][ii]] < 500:
            continue
        A_peak_list.append(A_peak[0][ii])
        # plt.plot(A_peak[0][ii], A_yvals[A_peak[0][ii]], '*', markersize=10)

    B_peak_list = []
    for ii in range(len(B_peak[0])):
        if B_yvals[B_peak[0][ii]] < 500:
            continue
        B_peak_list.append(B_peak[0][ii])
        # plt.plot(B_peak[0][ii], B_yvals[B_peak[0][ii]], '*', markersize=10)

    new_g_img = np.zeros(shape=A_g_img.shape, dtype=np.uint8)
    if (A_peak_list == []) | (B_peak_list == []):
        # 直接拉伸
        new_g_img, sign = gray_scale_stretching(A_yvals, B_yvals, A_g_img, B_g_img)
    else:
        max_A_peak = max(A_peak_list)
        max_B_peak = max(B_peak_list)
        if (max_A_peak < 15) | (max_B_peak < 15):
            # 直接拉伸
            new_g_img, sign = gray_scale_stretching(A_yvals, B_yvals, A_g_img, B_g_img)

        else:
            # 对比两peak值，进行peak移动
            if abs(max_A_peak - max_B_peak) <= 25:
                #     若两个peak相差小于10，直接拉伸
                new_g_img, sign = gray_scale_stretching(A_yvals, B_yvals, A_g_img, B_g_img)

            else:
                if max_A_peak > max_B_peak:
                    # peak_A较大,B图变换
                    trans_rate = max_A_peak / max_B_peak
                    sign = 'B'
                    for i in range(B_g_img.shape[0]):
                        for j in range(B_g_img.shape[1]):
                            new_g_img[i][j] = int(B_g_img[i][j] * trans_rate)
                            if new_g_img[i][j] > 255:
                                new_g_img[i][j] = 255
                    # 统计变换后等于255的像素的数量，如果大于10000个的就直接拉伸
                    hist, _ = np.histogram(new_g_img, bins=255)
                    num_255 = hist[-1]
                    if num_255 > 5000:
                        new_g_img, sign = gray_scale_stretching(A_yvals, B_yvals, A_g_img, B_g_img)


                elif max_A_peak < max_B_peak:
                    # peakB较大,A图变换
                    trans_rate = max_B_peak / max_A_peak
                    sign = 'A'
                    for i in range(A_g_img.shape[0]):
                        for j in range(A_g_img.shape[1]):
                            new_g_img[i][j] = int(A_g_img[i][j] * trans_rate)
                            if new_g_img[i][j] > 255:
                                new_g_img[i][j] = 255
                    # 统计变换后等于255的像素的数量，如果大于10000个的就直接拉伸
                    hist, _ = np.histogram(new_g_img, bins=255)
                    num_255 = hist[-1]
                    if num_255 > 5000:
                        new_g_img, sign = gray_scale_stretching(A_yvals, B_yvals, A_g_img, B_g_img)
    return new_g_img, sign


# if __name__ == '__main__':
#     csv_path = os.path.join('new_mix_1', 'mixed_csvs', 'img_comb1')
#     for csv_f in os.listdir(csv_path):
#         csv_f_path = os.path.join(csv_path, csv_f)
#         A_paths = pd.read_csv(csv_f_path)['cytosol'].values
#         B_paths = pd.read_csv(csv_f_path)['nucleoplasm'].values
#         m_ids = pd.read_csv(csv_f_path)['m_id'].values
#         fig_dir = os.path.join('img_fig', csv_f.replace('.csv', ''))
#         mkdir(fig_dir)
#         for i in range(len(A_paths)):
#
#             A_path_green = os.path.join(A_paths[i], 'green.jpg')
#             B_path_green = os.path.join(B_paths[i], 'green.jpg')
#             hist_fig_path = os.path.join(fig_dir, m_ids[i] + '.png')
#
#             A_g_img = cv2.imread(A_path_green, 0)
#             B_g_img = cv2.imread(B_path_green, 0)
#             draw_hist(A_g_img, B_g_img, hist_fig_path)
