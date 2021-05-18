import cv2
from PIL import Image
import numpy as np
import os
import pandas as pd

LABEL_NAMES = {
    0:  "nucleoplasm",
    1:  "nuclear membrane",
    2:  "nucleoli",
    3:  "nucleoli fibrillar center",
    4:  "nuclear speckles",
    5:  "nuclear bodies",
    6:  "endoplasmic reticulum",
    7:  "golgi apparatus",
    8:  "peroxisomes",
    9:  "endosomes",
    10:  "lysosomes",
    11:  "intermediate filaments",
    12:  "actin filaments",
    13:  "focal adhesion sites",
    14:  "microtubules",
    15:  "microtubule ends",
    16:  "cytokinetic bridge",
    17:  "mitotic spindle",
    18:  "microtubule organizing center",
    19:  "centrosome",
    20:  "lipid droplets",
    21:  "plasma membrane",
    22:  "cell junctions",
    23:  "mitochondria",
    24:  "aggresome",
    25:  "cytosol",
    26:  "cytoplasmic bodies",
    27:  "rods & rings",
    28:  "vesicles"
}

def mkdir(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print('---the ' + dirName + ' is created!---')
    else:
        print('---The dir is there!---')

def img_resize(img_path, img_save_path, img_size):
    img = img_path.split('\\')[-1]
    image = np.array(Image.open(img_path))
    image = cv2.resize(image, (img_size, img_size), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(os.path.join(img_save_path, img), image)

if __name__ == '__main__':
    comb_num = 1
    #  768 or 1536
    img_size = 768
    comb_name = 'img_comb' + str(comb_num)
    mix_imgs_dir = os.path.join('new_mix', 'mixed_concat_imgs', comb_name)
    img_save = os.path.join('mix_img_testset', comb_name + '_' + str(img_size))
    mkdir(img_save)
    mix_csv_path = os.path.join('new_mix', 'mixed_concat_imgs', comb_name + '.csv')
    csv_save_path = os.path.join('mix_img_testset', comb_name + '_' + str(img_size)+'.csv')
    Id = []
    Target = []
    M_rate = []
    comb_img_info = pd.read_csv(mix_csv_path)
    Id_imgs = comb_img_info['Id'].values
    Targe_labels = comb_img_info['Target'].values
    m_rates = comb_img_info['m_rate'].values
    for i in range(len(Id_imgs)):
        # get new label
        Targe_label = Targe_labels[i]
        Targe_num = []
        for label in Targe_label.split(','):
            if label in LABEL_NAMES.values():
                key = list(LABEL_NAMES.keys())[list(LABEL_NAMES.values()).index(label)]
                print(label, key)
                Targe_num.append(str(key))
            else:
                continue
        if Targe_num == []:
            continue
        else:
            labels = ' '.join(Targe_num)

        # img_resize and img_move
        img_Id = Id_imgs[i]
        m_rate = m_rates[i]
        g_m_path = os.path.join(mix_imgs_dir, m_rate, img_Id+'_green.jpg')
        b_m_path = os.path.join(mix_imgs_dir, m_rate, img_Id + '_blue.jpg')
        r_m_path = os.path.join(mix_imgs_dir, m_rate, img_Id + '_red.jpg')
        y_m_path = os.path.join(mix_imgs_dir, m_rate, img_Id + '_yellow.jpg')
        img_resize(g_m_path, img_save, img_size)
        img_resize(b_m_path, img_save, img_size)
        img_resize(r_m_path, img_save, img_size)
        img_resize(y_m_path, img_save, img_size)
        print(img_Id)
        Target.append(labels)
        Id.append(img_Id)
        M_rate.append(m_rate)


    dist = {'Id': Id, 'Target': Target, 'm_rate': M_rate}
    df = pd.DataFrame(data=dist, index=None, columns=['Id', 'Target', 'm_rate'])
    df.to_csv(csv_save_path, index=False)
    print('end!')