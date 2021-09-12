import os
import numpy as np
import cv2
from torch.utils.data.dataset import Dataset
from utils.common_util import *
import pandas as pd
from config.config import *
from datasets.tool import *
from utils.augment_util import *
from PIL import Image
import re

class ProteinDataset(Dataset):
    def __init__(self,
                 split_file,
                 img_dir,
                 img_size=512,
                 transform=None,
                 return_label=True,
                 is_trainset=True,
                 in_channels=4,
                 crop_size=0,
                 random_crop=False,
                 ):
        self.is_trainset = is_trainset
        self.img_size = img_size
        self.return_label = return_label
        self.in_channels = in_channels
        self.transform = transform
        self.crop_size = crop_size
        self.random_crop = random_crop
        split_df = pd.read_csv(split_file)
        if EXTERNAL not in split_df.columns:
            split_df[EXTERNAL] = False

        self.split_df = split_df
        if is_trainset:
            print(len(split_df))
            # self.labels = self.split_df[LABEL_NAME_LIST].values.astype(int)
            label_list = self.split_df[TARGET].values
            labels = np.zeros(shape=(len(self.split_df), len(LABEL_NAMES)))
            for i in range(len(label_list)):
                label_values = label_list[i].split()
                for label_value in label_values:
                    labels[i][int(label_value)] = 1
            self.labels = labels
            print(labels.shape)
            assert self.labels.shape == (len(self.split_df), len(LABEL_NAMES))

        self.is_external = self.split_df[EXTERNAL].values
        self.img_ids = self.split_df[ID].values
        self.num = len(self.img_ids)
        self.img_dir = img_dir


    def read_crop_img(self, img):
        random_crop_size = int(np.random.uniform(self.crop_size, self.img_size))
        x = int(np.random.uniform(0, self.img_size - random_crop_size))
        y = int(np.random.uniform(0, self.img_size - random_crop_size))
        crop_img = img[x:x + random_crop_size, y:y + random_crop_size]
        return crop_img

    def read_rgby(self, img_dir, img_id, index):
        if self.is_external[index]:
            img_is_external = True
        else:
            img_is_external = False

        # suffix = '.jpg' if img_is_external else '.png'
        suffix = '.jpg'
        if self.in_channels == 3:
            colors = ['red', 'green', 'blue']
        else:
            colors = ['red', 'green', 'blue', 'yellow']
        flags = cv2.IMREAD_GRAYSCALE
        img = [cv2.imread(opj(img_dir, img_id + '_' + color + suffix), flags)
               for color in colors]
        if self.in_channels == 2:
            img[0] = np.full(img[0].shape, 13.)
            img[3] = np.full(img[0].shape, 13.)
        img = np.stack(img, axis=-1)
        if self.random_crop and self.crop_size > 0:
            img = self.read_crop_img(img)
        return img

    def __getitem__(self, index):
        img_id = self.img_ids[index]
        img_id = str(img_id)

        if self.is_external[index]:
            img_dir = self.external_img_dir
        else:
            img_dir = self.img_dir

        image = self.read_rgby(img_dir, img_id, index)
        if image[0] is None:
            print(img_dir, img_id)

        h, w = image.shape[:2]
        if self.crop_size > 0:
            if self.crop_size != h or self.crop_size != w:
                image = cv2.resize(image, (self.crop_size, self.crop_size), interpolation=cv2.INTER_LINEAR)
        else:
            if self.img_size != h or self.img_size != w:
                image = cv2.resize(image, (self.img_size, self.img_size), interpolation=cv2.INTER_LINEAR)

        if self.transform is not None:
            image = self.transform(image)
        image = image / 255.0
        image = image_to_tensor(image)

        if self.return_label:
            label = self.labels[index]
            return image, label, index
        else:
            return image, index

    def __len__(self):
        return self.num
