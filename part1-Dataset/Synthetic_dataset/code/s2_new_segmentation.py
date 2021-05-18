import os
from PIL import Image
import pandas as pd
import numpy as np
from skimage import io,filters,segmentation,measure,morphology,color
import matplotlib.pyplot as plt

def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the '+dirName+' is created!---')
    else:
        print('---The dir is there!---')

def seg_samples(samples_dir, sample_csv, seg_dir):
    img_list = pd.read_csv(sample_csv) 
    sample_ids = img_list['sample_id'].values
    # label_ids = img_list['label'].values
    for sample in sample_ids:
        g_path = os.path.join(samples_dir, str(sample)+'_green.jpg')
        b_path = os.path.join(samples_dir, str(sample)+'_blue.jpg')
        r_path = os.path.join(samples_dir, str(sample)+'_red.jpg')
        y_path = os.path.join(samples_dir, str(sample)+'_yellow.jpg')
        m_path = os.path.join(samples_dir, str(sample)+'_mask.png')
        
        seg_path = os.path.join(seg_dir, str(sample))
        mkdir(seg_path)
        segment_img(g_path, b_path, y_path, r_path, m_path, seg_path)

def segment_img(g_path, b_path, y_path, r_path, m_path, seg_path):
    try:
        mask = io.imread(m_path)
        g1_img = io.imread(g_path)[:,:,1]
        b1_img = io.imread(b_path)[:,:,2]
        y1_img = np.asarray(Image.open(y_path).convert('L'))
        r1_img = io.imread(r_path)[:,:,0]

        image = color.rgb2gray(mask)
        thresh = filters.threshold_otsu(image)
        bw = morphology.opening(image > thresh, morphology.disk(3)) # circular kenel=3 with opening operation

        cleared = bw.copy()  # copy
        segmentation.clear_border(cleared)  # clear up the noise

        label_image = measure.label(cleared)  # label the region
        print(len(label_image))
        print(label_image.shape)

        i = 0
        for region in measure.regionprops(label_image): #循环得到每一个连通区域属性集

            # 忽略小区域
            if region.area < 10000:
                continue
            else:

                i = i+1
                bm = np.zeros(shape=label_image.shape)
                for coord in region.coords:
                    bm[coord[0], coord[1]] = 1

                g_img = bm * g1_img
                b_img = bm * b1_img
                y_img = bm * y1_img
                r_img = bm * r1_img
                # print(max(bm[:]))
                minr, minc, maxr, maxc = region.bbox
                g_patch = g_img[minr:maxr, minc:maxc]
                b_patch = b_img[minr:maxr, minc:maxc]
                y_patch = y_img[minr:maxr, minc:maxc]
                r_patch = r_img[minr:maxr, minc:maxc]
                bm_patch = bm[minr:maxr, minc:maxc]
                mkdir(os.path.join(seg_path, 'c' + str(i)))
                g_p = os.path.join(seg_path, 'c' + str(i), 'green.jpg')
                b_p = os.path.join(seg_path, 'c' + str(i), 'blue.jpg')
                y_p = os.path.join(seg_path, 'c' + str(i), 'yellow.jpg')
                r_p = os.path.join(seg_path, 'c' + str(i), 'red.jpg')
                m_p = os.path.join(seg_path, 'c' + str(i), 'mask.jpg')
                # io.imshow(g_patch)
                io.imsave(g_p, g_patch)
                io.imsave(b_p, b_patch)
                io.imsave(y_p, y_patch)
                io.imsave(r_p, r_patch)
                io.imsave(m_p, bm_patch)
    except OSError as reason:
        print('想要访问的文件不存在', '\n错误的原因是:', str(reason))

if __name__ == "__main__":
    # add segmentation dir
    seg_dir = 'new_segmentation'
    samples_dir = 'hgray_samples'
    sample_csv = 'hgray_samples.csv'
    # segmenting as cell images
    seg_samples(samples_dir, sample_csv, seg_dir)