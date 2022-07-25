#!/usr/bin/python

import os 
import numpy as np
import cv2 as cv

os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

def saveImage(filename, image):
    cv.imwrite(filename, image.astype(np.float32), [cv.IMWRITE_EXR_TYPE, cv.IMWRITE_EXR_TYPE_HALF])

def loadImage(filename, imreadFlags=None):
    return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))


# img = loadImage("skyangular_data/20140924_1.exr")
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# saveImage('convertOne.exr', img)
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# saveImage('convertTwo.exr', img)

label = cv.imread("train_label/20140924_1.png")
print(label.shape)