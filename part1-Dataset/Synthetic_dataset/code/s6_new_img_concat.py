import numpy as np
import cv2
import os
import math
import random
import pandas as pd

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
        print('---the ' + dirName + ' is created!---')
    else:
        print('---The dir is there!---')

def img_concat(img_path, m_slice_ids, img_save_path):
    blue_imgs = []
    green_imgs = []
    red_imgs = []
    yellow_imgs = []
    mask_imgs = []
    for m_slice_id in m_slice_ids:
        img_id_path = os.path.join(img_path, m_slice_id)
        print(img_id_path)
        mix_g_img = cv2.imread(img_id_path + '_green.jpg', 0)
        mix_b_img = cv2.imread(img_id_path + '_blue.jpg', 0)
        mix_r_img = cv2.imread(img_id_path + '_red.jpg', 0)
        mix_y_img = cv2.imread(img_id_path + '_yellow.jpg', 0)
        mix_m_img = cv2.imread(img_id_path + '_mask.jpg', 0)
        print('mix_b_img')
        print(mix_b_img.shape)
        blue_imgs.append(mix_b_img)
        green_imgs.append(mix_g_img)
        red_imgs.append(mix_r_img)
        yellow_imgs.append(mix_y_img)
        mask_imgs.append(mix_m_img)

    new_b_imgs, new_g_imgs, new_r_imgs, new_y_imgs, new_m_imgs = transform(blue_imgs, green_imgs,
                                                                           red_imgs, yellow_imgs,
                                                                           mask_imgs)
    b_img = concat(new_b_imgs)
    g_img = concat(new_g_imgs)
    r_img = concat(new_r_imgs)
    y_img = concat(new_y_imgs)
    m_img = concat(new_m_imgs)

    cv2.imwrite(img_save_path + '_blue.jpg', b_img)
    cv2.imwrite(img_save_path + '_green.jpg', g_img)
    cv2.imwrite(img_save_path + '_red.jpg', r_img)
    cv2.imwrite(img_save_path + '_yellow.jpg', y_img)
    cv2.imwrite(img_save_path + '_mask.jpg', m_img)


def transform(bimg_list, gimg_list, rimg_list, yimg_list, mimg_list):
    new_bimg_list = []
    new_gimg_list = []
    new_rimg_list = []
    new_yimg_list = []
    new_mimg_list = []

    for i in range(len(bimg_list)):
        bimg = bimg_list[i]
        gimg = gimg_list[i]
        rimg = rimg_list[i]
        yimg = yimg_list[i]
        mimg = mimg_list[i]

        # 由于所有通道图像的shape都一样，都为1024，所以这里随便选了bimg通道以得到shape信息
        rows, cols = bimg.shape
        row_cen = int(rows / 2)
        col_cen = int(cols / 2)
        new_row = 0
        new_col = 0
        num2 = random.randrange(0, 9)
        # print(num2)
        if num2 == 0:
            new_row = row_cen
            new_col = col_cen
        elif num2 == 1:
            new_row = row_cen + 200
            new_col = col_cen
        elif num2 == 2:
            new_row = row_cen - 200
            new_col = col_cen
        elif num2 == 3:
            new_row = row_cen
            new_col = col_cen + 200
        elif num2 == 4:
            new_row = row_cen
            new_col = col_cen - 200
        elif num2 == 5:
            new_row = row_cen + 128
            new_col = col_cen + 128
        elif num2 == 6:
            new_row = row_cen - 128
            new_col = col_cen - 128
        elif num2 == 7:
            new_row = row_cen - 128
            new_col = col_cen + 128
        elif num2 == 8:
            new_row = row_cen + 128
            new_col = col_cen - 128
        # 随意平移变换
        fir_arr = np.array([[row_cen, col_cen], [row_cen + 1, col_cen], [row_cen, col_cen + 1]], np.float32)
        sec_arr = np.array([[new_row, new_col], [new_row + 1, new_col], [new_row, new_col + 1]], np.float32)
        M = cv2.getAffineTransform(fir_arr, sec_arr)
        new_bimg = cv2.warpAffine(bimg, M, (rows, cols))
        new_gimg = cv2.warpAffine(gimg, M, (rows, cols))
        new_rimg = cv2.warpAffine(rimg, M, (rows, cols))
        new_yimg = cv2.warpAffine(yimg, M, (rows, cols))
        new_mimg = cv2.warpAffine(mimg, M, (rows, cols))

        # 随意旋转变换
        num1 = random.randrange(0, 5)
        R = cv2.getRotationMatrix2D((row_cen, col_cen), int(num1 * 60), 1.0)
        new_bimg = cv2.warpAffine(new_bimg, R, (rows, cols))
        new_gimg = cv2.warpAffine(new_gimg, R, (rows, cols))
        new_rimg = cv2.warpAffine(new_rimg, R, (rows, cols))
        new_yimg = cv2.warpAffine(new_yimg, R, (rows, cols))
        new_mimg = cv2.warpAffine(new_mimg, R, (rows, cols))

        new_bimg_list.append(new_bimg)
        new_gimg_list.append(new_gimg)
        new_rimg_list.append(new_rimg)
        new_yimg_list.append(new_yimg)
        new_mimg_list.append(new_mimg)

    return new_bimg_list, new_gimg_list, new_rimg_list, new_yimg_list, new_mimg_list

def concat(img_list):
    # 横向合并三张cell图，得到“三图合成图”
    conimg1 = np.concatenate((img_list[0], img_list[1], img_list[2]), axis=1)
    conimg2 = np.concatenate((img_list[3], img_list[4], img_list[5]), axis=1)
    conimg3 = np.concatenate((img_list[6], img_list[7], img_list[8]), axis=1)
    # 纵向合并三张“三图合成图”，得到一张9*9的新图
    conmix_img = np.concatenate((conimg1, conimg2, conimg3), axis=0)
    return conmix_img

if __name__ == "__main__":
    mixed_cell_dir = os.path.join('new_mix', 'mixed_imgs')
    mixed_csvs_dir = os.path.join('new_mix', 'mixed_csvs')
    mixed_concat_dir = os.path.join('new_mix', 'mixed_concat_imgs')
    m_samples_id = []
    m_labels_id = []
    m_rate = []
    m_c_id = 0
    # ----------------comb2-test----------------------------------------------------------------------
    # comb_id = 2
    # img_comb = 'img_comb' + str(comb_id)
    # mkdir(mixed_concat_dir)
    # csv_save_path = os.path.join(mixed_concat_dir, img_comb + '.csv')
    # for rate_id in range(1, 6):
    #
    #     rate = mix_rate['rate'+str(rate_id)]
    #     comb_rate = str(rate[0])+'_'+str(rate[1])
    #
    #     img_save = os.path.join(mixed_concat_dir, img_comb, comb_rate)
    #     mkdir(img_save)
    #
    #     img_path = os.path.join(mixed_cell_dir, img_comb, comb_rate)
    #     csv_path = os.path.join(mixed_csvs_dir, img_comb, comb_rate + '.csv')
    #     m_ids = pd.read_csv(csv_path)['m_id'].values
    #     # random.shuffle(m_ids)
    #     for i in range(int(len(m_ids)/9)):
    #         img_save_path = os.path.join(img_save, 'mixed_img' + str(m_c_id))
    #         m_slice_ids = m_ids[(i*9): ((i+1)*9)]
    #         print(img_path)
    #         img_concat(img_path, m_slice_ids, img_save_path)
    #         m_samples_id.append('mixed_img'+str(m_c_id))
    #         if comb_rate == '1_0':
    #             m_labels_id.append(combination[comb_id][0])
    #         elif comb_rate == '0_1':
    #             m_labels_id.append(combination[comb_id][1])
    #         else:
    #             m_labels_id.append(combination[comb_id][0] + ',' + combination[comb_id][1])
    #         m_labels_id.append(combination[comb_id][0] + ',' + combination[comb_id][1])
    #         m_rate.append(comb_rate)
    #         m_c_id = m_c_id + 1
    # -------------------------------all----------------------------------------------------------------
    for comb_id in range(1, 6):
        mkdir(mixed_concat_dir)
        img_comb = 'img_comb' + str(comb_id)
        csv_save_path = os.path.join(mixed_concat_dir, img_comb + '.csv')
        for rate_id in range(1, 6):

            rate = mix_rate['rate'+str(rate_id)]
            comb_rate = str(rate[0])+'_'+str(rate[1])

            img_save = os.path.join(mixed_concat_dir, img_comb, comb_rate)
            mkdir(img_save)

            img_path = os.path.join(mixed_cell_dir, img_comb, comb_rate)
            csv_path = os.path.join(mixed_csvs_dir, img_comb, comb_rate + '.csv')
            m_ids = pd.read_csv(csv_path)['m_id'].values
            # random.shuffle(m_ids)
            for i in range(int(len(m_ids)/9)):
                img_save_path = os.path.join(img_save, 'mixed_img' + str(m_c_id))
                m_slice_ids = m_ids[(i*9): ((i+1)*9)]
                img_concat(img_path, m_slice_ids, img_save_path)
                m_samples_id.append('mixed_img'+str(m_c_id))
                if comb_rate == '1_0':
                    m_labels_id.append(combination[comb_id][0])
                elif comb_rate == '0_1':
                    m_labels_id.append(combination[comb_id][1])
                else:
                    m_labels_id.append(combination[comb_id][0] + ',' + combination[comb_id][1])
                m_rate.append(comb_rate)
                m_c_id = m_c_id + 1

        dist = {'Id': m_samples_id, 'Target': m_labels_id, 'm_rate': m_rate}
        df = pd.DataFrame(data=dist, index=None, columns=['Id', 'Target', 'm_rate'])
        df.to_csv(csv_save_path, index=False)
        m_samples_id = []
        m_labels_id = []
        m_rate = []
