#!/usr/bin/python
import os
import sys
from glob import glob

import numpy as np
import cv2 as cv
from PIL import Image

data_paths_hdr = glob("clouds_clean_toy/*.exr")
data_paths_labels = glob("masks_cc_toy/*.png")

os.environ["OPENCV_IO_ENABLE_OPENEXR"]="1"

def saveImage(filename, image):
    cv.imwrite(filename, image.astype(np.float32), [cv.IMWRITE_EXR_TYPE, cv.IMWRITE_EXR_TYPE_HALF])

def loadImage(filename, imreadFlags=None):
    return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))

def __rand_rotate(img, rand_rotate):
    return img.rotate(angle=rand_rotate)

for h, l in zip(data_paths_hdr, data_paths_labels):
    label = Image.open(l)

    hdr = loadImage(h)
    image = np.asarray(hdr)
    image = Image.fromarray(image.astype(np.uint8))

    rand_rotate = np.random.randint(0,360)
    label_rot = __rand_rotate(label, rand_rotate)
    image_rot = np.array(__rand_rotate(image, rand_rotate))

    label_rot.save(f"rr_masks_cc_toy/{l[13:]}")
    saveImage(f"rr_clouds_clean_toy/{h[17:]}", image_rot)

    print(f"Done: {l[13:]} & {h[17:]}")