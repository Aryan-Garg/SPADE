#!/usr/bin/python

import os
import cv2 as cv
import numpy as np

os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

REAL_IMG_PATH=f"checkpoints/full_toy/web/images/real"
FAKE_IMG_PATH=f"checkpoints/full_toy/web/images/synth"

path_parent = os.path.dirname(os.getcwd())

def loadImage(filename, imreadFlags=None):
    return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))

def reader(out_path):
    for f in os.listdir(out_path):
        img = loadImage(out_path+"/"+f)
        print(f"filename: {f} | max: {img.max()} | min: {img.min()}")
        # print("NaN vals:", np.isnan(img))

reader(path_parent+"/"+REAL_IMG_PATH)
reader(path_parent+"/"+FAKE_IMG_PATH)
        