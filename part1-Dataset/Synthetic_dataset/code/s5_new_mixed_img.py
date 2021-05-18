import numpy as np
import os,shutil
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from hist_regul import *


combination = {1: ['cytosol', 'nucleoplasm'],
               2: ['cytosol', 'plasma membrane'],
               3: ['nucleoplasm', 'vesicles'],
               4: ['nucleoli', 'nucleoplasm'],
               5: ['mitochondria', 'nucleoplasm']}

mix_rate = {
    'rate1': [1, 0],
    'rate2': [0.25, 0.75],
    'rate3': [0.5, 0.5],
    'rate4': [0.75, 0.25],
    'rate5': [0, 1]
}


def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the '+dirName+' is created!---')
    else:
        print('---The dir is there!---')

def stop_ind(list, begin_ind):
    ind_list = []
    ind_list.append(begin_ind)
    sub_list_len = int((len(list)-begin_ind)/3)
    ind = begin_ind
    for i in range(3):
        ind = ind + sub_list_len
        if ind > (len(list)):
            break
        ind_list.append(ind)
    return ind_list, sub_list_len


def get_center(b_mask_path):
    # print(b_mask_path)
    b_mask = cv2.imread(b_mask_path, 0)
    cnts, h = cv2.findContours(b_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    area = []
    for c in cnts:
        area.append(cv2.contourArea(c))
    cnt_max = cnts[np.argsort(-np.array(area))[0]]
    M = cv2.moments((cnt_max))
    centerX = M['m10'] / M['m00']
    centerY = M['m01'] / M['m00']
    return centerX, centerY



def draw_hist(A_g_img, B_g_img, hist_fig_path):
    plt.figure()
    plt.subplot(221)
    plt.imshow(A_g_img, cmap=plt.cm.gray)

    plt.subplot(222)
    plt.hist(A_g_img.ravel(), 255, [1, 256])

    plt.subplot(223)
    plt.imshow(B_g_img, cmap=plt.cm.gray)
    plt.subplot(224)

    plt.hist(B_g_img.ravel(), 255, [1, 256])
    plt.savefig(hist_fig_path)
    plt.show()



def img_pure(label, pure_paths, mixed_csv, img_save_dir):
    print(len(pure_paths))
    csv_pure_path = []
    m_id = []
    j = 0
    for i in range(len(pure_paths)):

        pure_path = pure_paths[i]
        if not os.path.exists(pure_path):
            print('The pure_path is missing!')
            continue
        try:
            g_img_path = os.path.join(pure_path, 'green.jpg')
            b_img_path = os.path.join(pure_path, 'blue.jpg')
            r_img_path = os.path.join(pure_path, 'red.jpg')
            y_img_path = os.path.join(pure_path, 'yellow.jpg')
            m_img_path = os.path.join(pure_path, 'mask.jpg')

            shutil.copy(g_img_path, os.path.join(img_save_dir, 'm' + str(j) + '_green.jpg'))
            shutil.copy(b_img_path, os.path.join(img_save_dir, 'm' + str(j) + '_blue.jpg'))
            shutil.copy(r_img_path, os.path.join(img_save_dir, 'm' + str(j) + '_red.jpg'))
            shutil.copy(y_img_path, os.path.join(img_save_dir, 'm' + str(j) + '_yellow.jpg'))
            shutil.copy(m_img_path, os.path.join(img_save_dir, 'm' + str(j) + '_mask.jpg'))
            csv_pure_path.append(pure_path)
            m_id.append('m' + str(j))
            j = j + 1
        except ValueError:
            print('Pure sample ValueError!')
            continue
        except IndexError:
            print('Pure sample IndexError!')
            continue
    dist = {'m_id': m_id, label: csv_pure_path}
    df = pd.DataFrame(data=dist, index=None, columns=['m_id', label])
    df.to_csv(mixed_csv, index=False)

def img_mix(labelA, labelB, A_paths, B_paths, A_rate, B_rate, mixed_csv, img_save_dir):
    print('the lenght of A_paths: %d'%len(A_paths))
    print('the lenght of B_paths: %d'%len(B_paths))
    csv_A_path = []
    csv_B_path = []
    m_id = []
    m_rate = []
    j = 0
    for i in range(len(A_paths)):

        A_path = A_paths[i]
        print(A_path)
        if not os.path.exists(A_path):
            print('The A_path is missing!')
            continue
        try:
            if not os.path.exists(os.path.join(A_path, 'mask.jpg')):
                # print('The '+os.path.join(A_path, 'mask.jpg')+' is missing!')
                continue
            A_mask = cv2.cvtColor(cv2.imread(os.path.join(A_path, 'mask.jpg')), cv2.COLOR_BGR2GRAY)
            A_centerX, A_centerY = get_center(os.path.join(A_path, 'b_mask.jpg'))
            for n in range(len(B_paths)):
                B_path = B_paths[n]
                if not os.path.exists(B_path):
                    # print('The B_path is missing!')
                    continue
                try:
                    if not os.path.exists(os.path.join(B_path, 'mask.jpg')):
                        # print('The '+os.path.join(B_path, 'mask.jpg')+' is missing!')
                        continue
                    B_mask = cv2.cvtColor(cv2.imread(os.path.join(B_path, 'mask.jpg')), cv2.COLOR_BGR2GRAY)
                    B_centerX, B_centerY = get_center(os.path.join(B_path, 'b_mask.jpg'))

                    A_arr = np.array([[A_centerX, A_centerY], [A_centerX + 1, A_centerY], [A_centerX, A_centerY + 1]], np.float32)
                    B_arr = np.array([[B_centerX, B_centerY], [B_centerX + 1, B_centerY], [B_centerX, B_centerY + 1]], np.float32)
                    M = cv2.getAffineTransform(A_arr, B_arr)
                    rows, cols = A_mask.shape[:2]
                    tran_A_mask = cv2.warpAffine(A_mask, M, (rows, cols))
                    mix_mask = cv2.addWeighted(tran_A_mask, 0.5, B_mask, 0.5, 0)
                    if np.max(mix_mask) != 255:
                        print('Mixing error!!')
                        continue
                    hist, bins = np.histogram(mix_mask, bins=255)
                    total_area = sum(hist[128:255])
                    dst_area = hist[-1]
                    area_p = float(dst_area) / total_area

                    if area_p >= 0.75:
                        if (A_path in csv_A_path) | (B_path in csv_B_path):
                            print(A_path + ' or ' + B_path + 'is exist!')
                            continue
                        print('A_path: %s' % A_path)
                        print('B_path: %s' % B_path)
                        print('area_rate: %f' % area_p)
                        A_g_img = cv2.imread(os.path.join(A_path, 'green.jpg'),0)
                        B_g_img = cv2.imread(os.path.join(B_path, 'green.jpg'),0)
                        # hist_fig_path = os.path.join('plt_figure', 'm' + str(j) + ".png")
                        # 图像的灰度均衡
                        new_g_img, sign = gray_hist_regulation(A_g_img, B_g_img)
                        # 若sign == ‘A’，则new_g_img代表A_g_img；若sign == ‘B’，则new_g_img代表B_g_img
                        if sign == 'A':
                            A_g_img = new_g_img
                        elif sign == 'B':
                            B_g_img = new_g_img
                        # print(sign)
                        # print(A_g_img.dtype)
                        # print(B_g_img.dtype)
                        tran_A_green = cv2.warpAffine(A_g_img, M, (rows, cols))
                        mix_g_img = cv2.addWeighted(tran_A_green, A_rate, B_g_img, B_rate, 0)

                        A_b_img = cv2.imread(os.path.join(A_path, 'blue.jpg'),0)
                        B_b_img = cv2.imread(os.path.join(B_path, 'blue.jpg'),0)
                        tran_A_blue = cv2.warpAffine(A_b_img, M, (rows, cols))
                        mix_b_img = cv2.addWeighted(tran_A_blue, A_rate, B_b_img, B_rate, 0)

                        cv2.imwrite(os.path.join(img_save_dir, 'm' + str(j) + '_mask.jpg'), mix_mask)
                        cv2.imwrite(os.path.join(img_save_dir, 'm'+str(j)+'_green.jpg'), mix_g_img)
                        cv2.imwrite(os.path.join(img_save_dir, 'm'+str(j)+'_blue.jpg'), mix_b_img)

                        if A_rate >= B_rate:
                            A_r_path = os.path.join(A_path, 'red.jpg')
                            A_y_path = os.path.join(A_path, 'yellow.jpg')
                            shutil.copy(A_r_path, os.path.join(img_save_dir, 'm' + str(j) + '_red.jpg'))
                            shutil.copy(A_y_path, os.path.join(img_save_dir, 'm' + str(j) + '_yellow.jpg'))
                        else:
                            B_r_path = os.path.join(B_path, 'red.jpg')
                            B_y_path = os.path.join(B_path, 'yellow.jpg')
                            shutil.copy(B_r_path, os.path.join(img_save_dir, 'm' + str(j) + '_red.jpg'))
                            shutil.copy(B_y_path, os.path.join(img_save_dir, 'm' + str(j) + '_yellow.jpg'))
                        csv_A_path.append(A_path)
                        csv_B_path.append(B_path)
                        m_id.append('m'+str(j))
                        m_rate.append(area_p)
                        j = j+1

                except ValueError:
                    print('Blabel sample ValueError!')
                    continue
                except IndexError:
                    print('Blabel sample IndexError!')
                    continue
        except ValueError:
            print('Alabel sample ValueError!')
            continue
        except IndexError:
            print('Alabel sample IndexError!')
            continue
        except FileNotFoundError as e:
            print(e)
            continue
    dist = {'m_id': m_id, labelA: csv_A_path, labelB: csv_B_path, 'm_rate': m_rate}
    df = pd.DataFrame(data=dist, index=None, columns=['m_id', labelA, labelB, 'm_rate'])
    df.to_csv(mixed_csv, index=False)

def read_comb_path(comb_path, Alabel, Blabel):
    A_paths = []
    B_paths = []
    f = open(comb_path, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.replace('\n', '')
        paths = line.split(',')
        if paths[0] == Alabel:
            A_paths = paths[1:]
        elif paths[0] == Blabel:
            B_paths = paths[1:]
    return A_paths, B_paths


if __name__ == "__main__":
    img_dir = 'new_transform'
    mix_dir = 'new_mix'
    # mixed_rate
    rate_key = 'rate4'
    # combination id
    i = 3
    begin_ind = 70
    comb_path = os.path.join('path_txt', 'path_comb'+str(i)+'.txt')
    A_paths, B_paths = read_comb_path(comb_path, combination[i][0], combination[i][1])

    A_stop_ind, A_slice_len = stop_ind(A_paths, begin_ind)
    B_stop_ind, B_slice_len = stop_ind(B_paths, begin_ind)
#--------------------RATE1=[0, 1]---------------------------------------------------------------------------------------
    if rate_key == 'rate1':
        rate_value = mix_rate[rate_key]
        A_paths = A_paths[A_stop_ind[0]-begin_ind: A_stop_ind[0]]

        csv_path = os.path.join(mix_dir, 'mixed_csvs', 'img_comb' + str(i))
        mkdir(csv_path)
        mixed_csv = os.path.join(csv_path, str(rate_value[0]) + '_' + str(rate_value[1]) + '.csv')

        img_save_dir = os.path.join(mix_dir, 'mixed_imgs', 'img_comb' + str(i), str(rate_value[0]) + '_' + str(rate_value[1]))
        mkdir(img_save_dir)
        img_pure(combination[i][0], A_paths, mixed_csv, img_save_dir)
#--------------------RATE2=[0.25, 0.75]---------------------------------------------------------------------------------
    elif rate_key == 'rate2':
        rate_value = mix_rate[rate_key]
        A_paths = A_paths[A_stop_ind[0]: A_stop_ind[1]]
        B_paths = B_paths[B_stop_ind[0]: B_stop_ind[1]]
        csv_path = os.path.join(mix_dir, 'mixed_csvs', 'img_comb' + str(i))
        mkdir(csv_path)
        mixed_csv = os.path.join(csv_path, str(rate_value[0]) + '_' + str(rate_value[1]) + '.csv')

        img_save_dir = os.path.join(mix_dir, 'mixed_imgs', 'img_comb' + str(i), str(rate_value[0]) + '_' + str(rate_value[1]))
        mkdir(img_save_dir)

        img_mix(combination[i][0], combination[i][1], A_paths, B_paths, rate_value[0], rate_value[1], mixed_csv,
                img_save_dir)
#--------------------RATE3=[0.5, 0.5]-----------------------------------------------------------------------------------
    elif rate_key == 'rate3':
        rate_value = mix_rate[rate_key]
        A_paths = A_paths[A_stop_ind[1]: A_stop_ind[2]]
        B_paths = B_paths[B_stop_ind[1]: B_stop_ind[2]]
        csv_path = os.path.join(mix_dir, 'mixed_csvs', 'img_comb' + str(i))
        mkdir(csv_path)
        mixed_csv = os.path.join(csv_path, str(rate_value[0]) + '_' + str(rate_value[1]) + '.csv')

        img_save_dir = os.path.join(mix_dir, 'mixed_imgs', 'img_comb' + str(i), str(rate_value[0]) + '_' + str(rate_value[1]))
        mkdir(img_save_dir)

        img_mix(combination[i][0], combination[i][1], A_paths, B_paths, rate_value[0], rate_value[1], mixed_csv,
                img_save_dir)
#--------------------RATE4=[0.75, 0.25]---------------------------------------------------------------------------------
    elif rate_key == 'rate4':
        rate_value = mix_rate[rate_key]
        A_paths = A_paths[A_stop_ind[2]: A_stop_ind[3]]
        B_paths = B_paths[B_stop_ind[2]: B_stop_ind[3]]
        csv_path = os.path.join(mix_dir, 'mixed_csvs', 'img_comb' + str(i))
        mkdir(csv_path)
        mixed_csv = os.path.join(csv_path, str(rate_value[0]) + '_' + str(rate_value[1]) + '.csv')

        img_save_dir = os.path.join(mix_dir, 'mixed_imgs', 'img_comb' + str(i), str(rate_value[0]) + '_' + str(rate_value[1]))
        mkdir(img_save_dir)

        img_mix(combination[i][0], combination[i][1], A_paths, B_paths, rate_value[0], rate_value[1], mixed_csv,
                img_save_dir)
#--------------------RATE5=[0, 1]---------------------------------------------------------------------------------------
    elif rate_key == 'rate5':
        rate_value = mix_rate[rate_key]
        B_paths = B_paths[B_stop_ind[0] - begin_ind: B_stop_ind[0]]

        csv_path = os.path.join(mix_dir, 'mixed_csvs', 'img_comb' + str(i))
        mkdir(csv_path)
        mixed_csv = os.path.join(csv_path, str(rate_value[0]) + '_' + str(rate_value[1]) + '.csv')

        img_save_dir = os.path.join(mix_dir, 'mixed_imgs', 'img_comb' + str(i), str(rate_value[0]) + '_' + str(rate_value[1]))
        mkdir(img_save_dir)
        img_pure(combination[i][1], B_paths, mixed_csv, img_save_dir)

