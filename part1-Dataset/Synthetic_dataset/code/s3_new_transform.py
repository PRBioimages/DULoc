import os
import cv2
import pandas as pd
from PIL import Image,ImageOps
import numpy as np
import math
from scipy import spatial

label_list = ['nucleoplasm', 'cytosol', 'mitochondria', 'vesicles', 'plasma membrane', 'nucleoli']

def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the '+dirName+' is created!---')
    else:
        print('---The dir is there!---')

def read_data(seg_dir, save_dir, sam_csv, new_sam_csv):
    img_infos = pd.read_csv(sam_csv)
    samples = img_infos['sample_id']
    labels = img_infos['label']
    new_samples = []
    new_labels = []
    for i in range(len(samples)):
        if labels[i] in label_list:
            cells_list = os.listdir(os.path.join(seg_dir, str(samples[i])))
            new_samples.append(str(samples[i]))
            new_labels.append(labels[i])
            for cell in cells_list:
                mkdir(os.path.join(save_dir, str(samples[i]), cell))
                # # eg. img == 'green.jpg'
                b_path = os.path.join(seg_dir, str(samples[i]), cell, 'blue.jpg')
                g_path = os.path.join(seg_dir, str(samples[i]), cell, 'green.jpg')
                y_path = os.path.join(seg_dir, str(samples[i]), cell, 'yellow.jpg')
                r_path = os.path.join(seg_dir, str(samples[i]), cell, 'red.jpg')
                m_path = os.path.join(seg_dir, str(samples[i]), cell, 'mask.jpg')
                try:
                    transform_img(b_path, g_path, y_path, r_path, m_path, seg_dir, save_dir)
                except ValueError:
                    print('ValueError!')
                    continue
                except IndexError:
                    print('IndexError!')
                    continue
        else:
            continue
    dist = {'sample_id':new_samples, 'label':new_labels}
    df = pd.DataFrame(data=dist, index=None, columns=['sample_id', 'label'])
    df.to_csv(new_sam_csv, index=False)

def degree_calculate(img_path):
    print(img_path)
    b_img = cv2.imread(img_path,0)

    _, img_bw = cv2.threshold(b_img, 30, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    img_bw = cv2.morphologyEx(img_bw, cv2.MORPH_OPEN, kernel)
    img_bw = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, kernel)
    cnts, h = cv2.findContours(img_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    area = []
    for c in cnts:
        area.append(cv2.contourArea(c))
    cnt_max = cnts[np.argsort(-np.array(area))[0]]
    cnt_max = np.reshape(cnt_max, (-1, 2))
    dist_mat = spatial.distance_matrix(cnt_max, cnt_max)
    i, j = np.unravel_index(dist_mat.argmax(), dist_mat.shape)
    x1 = cnt_max[i][0]
    y1 = cnt_max[i][1]
    x2 = cnt_max[j][0]
    y2 = cnt_max[j][1]
    degree = 0
    if x1 == x2:
        degree = 90
    else:
        rad = math.atan((y1 - y2) / (x1 - x2))
        degree = math.degrees(rad)
    return img_bw, degree, cnt_max[i], cnt_max[j]

def transform_img(b_path, g_path, y_path, r_path, m_path, seg_dir, save_dir):
    b_bw, degree, ord1, ord2 = degree_calculate(b_path)
    print(degree)

    b_im = Image.open(b_path)
    b_bw_im = Image.fromarray(b_bw)
    g_im = Image.open(g_path)
    y_im = Image.open(y_path)
    r_im = Image.open(r_path)
    m_im = Image.open(m_path)

    # rotate + padding
    rotate_b_img = b_im.rotate(degree, expand=True)
    rotate_b_bw_img = b_bw_im.rotate(degree, expand=True)
    rotate_g_img = g_im.rotate(degree, expand=True)
    rotate_y_img = y_im.rotate(degree, expand=True)
    rotate_r_img = r_im.rotate(degree, expand=True)
    rotate_m_img = m_im.rotate(degree, expand=True)

    # crop and padding to 1024*1024
    w = rotate_b_img.size[0]
    h = rotate_b_img.size[1]
    pr=0;pc=0;cr=0;cc=0
    r = int(math.fabs(1024-w)/2+0.5)
    c = int(math.fabs(1024-h)/2+0.5)
    if w <= 1024:
        pr = r
    else:
        cr = r
    if h <= 1024:
        pc = c
    else:
        cc = c
    crop_b_img = ImageOps.crop(rotate_b_img, (cr, cc, cr, cc))
    crop_b_bw_img = ImageOps.crop(rotate_b_bw_img, (cr, cc, cr, cc))
    crop_g_img = ImageOps.crop(rotate_g_img, (cr, cc, cr, cc))
    crop_y_img = ImageOps.crop(rotate_y_img, (cr, cc, cr, cc))
    crop_r_img = ImageOps.crop(rotate_r_img, (cr, cc, cr, cc))
    crop_m_img = ImageOps.crop(rotate_m_img, (cr, cc, cr, cc))

    pad_b_img = ImageOps.expand(crop_b_img, (pr, pc, pr, pc))
    pad_b_bw_img = ImageOps.expand(crop_b_bw_img, (pr, pc, pr, pc))
    pad_g_img = ImageOps.expand(crop_g_img, (pr, pc, pr, pc))
    pad_y_img = ImageOps.expand(crop_y_img, (pr, pc, pr, pc))
    pad_r_img = ImageOps.expand(crop_r_img, (pr, pc, pr, pc))
    pad_m_img = ImageOps.expand(crop_m_img, (pr, pc, pr, pc))

    resize_b_img = pad_b_img.resize((1024, 1024), Image.ANTIALIAS)
    resize_b_bw_img = pad_b_bw_img.resize((1024, 1024), Image.ANTIALIAS)
    resize_g_img = pad_g_img.resize((1024, 1024), Image.ANTIALIAS)
    resize_y_img = pad_y_img.resize((1024, 1024), Image.ANTIALIAS)
    resize_r_img = pad_r_img.resize((1024, 1024), Image.ANTIALIAS)
    resize_m_img = pad_m_img.resize((1024, 1024), Image.ANTIALIAS)

    resize_b_img = np.array(resize_b_img).astype(np.uint8)
    resize_b_bw_img = np.array(resize_b_bw_img).astype(np.int)
    resize_g_img = np.array(resize_g_img).astype(np.uint8)
    resize_y_img = np.array(resize_y_img).astype(np.uint8)
    resize_r_img = np.array(resize_r_img).astype(np.uint8)
    resize_m_img = np.array(resize_m_img).astype(np.uint8)
    # print(resize_b_img.shape)
    t_b_p = b_path.replace(seg_dir, save_dir)
    t_b_bw_p = t_b_p.replace('blue.jpg', 'b_mask.jpg')
    t_g_p = g_path.replace(seg_dir, save_dir)
    t_y_p = y_path.replace(seg_dir, save_dir)
    t_r_p = r_path.replace(seg_dir, save_dir)
    t_m_p = m_path.replace(seg_dir, save_dir)

    cv2.imwrite(t_b_p, resize_b_img)
    cv2.imwrite(t_b_bw_p, resize_b_bw_img)
    cv2.imwrite(t_g_p, resize_g_img)
    cv2.imwrite(t_y_p, resize_y_img)
    cv2.imwrite(t_r_p, resize_r_img)
    cv2.imwrite(t_m_p, resize_m_img)

if __name__ == "__main__":
    seg_dir = 'new_segmentation'
    trans_dir = 'new_transform'
    sam_csv = 'hgray_samples.csv'
    new_sam_csv = 'final.csv'
    # transform the cell images with same centers sad size
    read_data(seg_dir, trans_dir, sam_csv, new_sam_csv)