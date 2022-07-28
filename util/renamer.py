#!/usr/bin/python

import os
import shutil

# MV 
import cv2 as cv
import numpy as np

# Enable EXR
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

fileName = '20150606_170443_050_359_HDR.exr'

def saveImage(filename, image):
    cv.imwrite(filename, image.astype(np.float32), [cv.IMWRITE_EXR_TYPE, cv.IMWRITE_EXR_TYPE_HALF])

def loadImage(filename, imreadFlags=None):
    return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))

count = 1
for imgName in os.listdir(os.getcwd()):
    if '.exr' in imgName:
        img = loadImage(imgName)
        saveImage(imgName[:9] + str(count) + ".exr", img)
        os.remove(imgName)
        print(count)
        count += 1
        
