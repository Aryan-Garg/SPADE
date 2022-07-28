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

for f in os.listdir(os.getcwd()):
    img = loadImage(f)
    img = tm.tm_model.tonemap(img)
    saveImage("tm_log2_" + f, img)