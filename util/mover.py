#!/usr/bin/python

import os
import sys
import shutil

# MV 
import cv2 as cv
import numpy as np

curr = os.getcwd()
for f in os.listdir(curr):
    if "itmLG2" in f or "real" in f or "png" in f:
        continue

    if "N" in f and "synthesized" in f:
        shutil.move(curr + "/" + f, curr + "/synth/" + f)

