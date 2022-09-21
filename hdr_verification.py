#!/usr/bin/python

import os
import shutil
from turtle import done

# MV 
import cv2 as cv
import numpy as np


jimbo_path = "checkpoints/jimbo_full_100/web/images/synth"
save_path = "checkpoints/hdr_verification"

if not os.path.exists(save_path):
    os.mkdir(save_path)
else:
    shutil.rmtree(save_path)
    os.mkdir(save_path)
    
# Enable EXR
os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

def saveImage(filename, image):
    cv.imwrite(filename, image.astype(np.float32), [cv.IMWRITE_EXR_TYPE, cv.IMWRITE_EXR_TYPE_HALF])

def loadImage(filename, imreadFlags=None):
    return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))

dividers = [5,10,20,100,1000]

for divider in dividers:
    print(f"Divider: {divider}")
    for f in os.listdir(jimbo_path):
        if not "gamma" in f and "itmLG2" in f and ".exr" in f:
            img = loadImage(jimbo_path + "/" + f)
            img /= divider
            saveImage(save_path + f"/div{divider}_" + f, img)
            print("[Saved]: ", save_path + "/" + f)
    print("-------------------------------")