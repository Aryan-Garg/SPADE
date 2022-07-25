#!/usr/bin/python

import os 
from shutil import copy
import random 
from tqdm import tqdm

dirList = ['train_img', 'test_img', 'test_label', 'train_label']

for dirPath in dirList:
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)


partition_percentage = 80
annotations_dir = 'masks_2016'
img_dir = 'skyangular_data_2016'
annotations_files = os.listdir(annotations_dir)
annotations_files = [os.path.join(os.path.realpath("."), annotations_dir, x) for x in annotations_files]

train_labels = random.sample(annotations_files, int(partition_percentage / 100 * len(annotations_files)))
test_labels   = [x for x in annotations_files if x not in train_labels]

train_images = [x.replace("masks_2016", "skyangular_data_2016").replace("mask_", "").replace(".png", ".exr") for x in train_labels]
test_images  = [x.replace("masks_2016", "skyangular_data_2016").replace("mask_", "").replace(".png", ".exr") for x in test_labels]


# print(test_labels)
# print("-----------------\n\n")
# print(test_images)

for file in tqdm(train_labels):
    src = file
    dst = file.replace(annotations_dir, 'train_label').replace("mask_", "")
    copy(src, dst)


for file in tqdm(test_labels):
    src = file
    dst = file.replace(annotations_dir, 'test_label').replace("mask_", "")
    copy(src, dst)

for file in tqdm(train_images):
    src = file
    dst = file.replace(img_dir, 'train_img')
    copy(src, dst)
    
for file in tqdm(test_images):
    src = file
    dst = file.replace(img_dir, 'test_img')
    copy(src, dst)