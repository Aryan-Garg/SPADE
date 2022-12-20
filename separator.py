#!/usr/bin/python
import os
import sys
import shutil

import numpy as np
import cv2 as cv

try:
    exp_name = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <experiment_name>")

exp_path = f"checkpoints/{exp_name}/web/images/"

if not os.path.exists(exp_path + "synth"):
    os.mkdir(exp_path + "synth/")

if not os.path.exists(exp_path + "masks"):
    os.mkdir(exp_path + "masks/")

if not os.path.exists(exp_path + "real"):
    os.mkdir(exp_path + "real/")

if not os.path.exists(exp_path + "INVreal"):
    os.mkdir(exp_path + "INVreal/")

if not os.path.exists(exp_path + "INVsynth"):
    os.mkdir(exp_path + "INVsynth/")

for img_name in os.listdir(exp_path):
    if "label.png" in img_name:
        os.rename(exp_path + img_name, exp_path + "masks/" + img_name)
    
    elif "itmLG2" in img_name:
        if "real" in img_name:
            os.rename(exp_path + img_name, exp_path + "INVreal/" + img_name)
        else:
            os.rename(exp_path + img_name, exp_path + "INVsynth/" + img_name)

    elif "real_image.exr" in img_name:
        os.rename(exp_path + img_name, exp_path + "real/" + img_name)
    
    elif "synthesized_image.exr" in img_name:
        os.rename(exp_path + img_name, exp_path + "synth/" + img_name)
    
    elif "histogram" in img_name:
        os.rename(exp_path + img_name, exp_path + "INVsynth/" + img_name)
