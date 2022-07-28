#!/usr/bin/python

import os
import sys

# MV 
import cv2 as cv
import numpy as np

# Custom
import tonemap as tm

os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

def saveImage(filename, image):
    cv.imwrite(filename, image.astype(np.float32), [cv.IMWRITE_EXR_TYPE, cv.IMWRITE_EXR_TYPE_HALF])

def loadImage(filename, imreadFlags=None):
    return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))

def normalize_minMax(data):
    if data.ndim > 2:
        for i in range(data.shape[-1]):
            data[:,:,i] = (data[:,:,i] - np.min(data[:,:,i])) / (np.max(data[:,:,i]) - np.min(data[:,:,i]))
    else: 
        data = (data - np.min(data)) / (np.max(data) - np.min(data))
    return data

for f in os.listdir(os.getcwd()):
    if '.exr' in f:
        print(f)
        img = loadImage(f)
        img = normalize_minMax(img)
        saveImage('N_' + f, img)