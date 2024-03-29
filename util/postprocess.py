#!/usr/bin/python

import os
import sys

# MV 
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Custom
from . import tonemap as tm


path_parent = os.path.dirname(os.getcwd())

class PostProcessor():
    # Control Flow Overview:
    # Normalizes -> Inv-log2 Tms -> Gamma Tms
    
    def __init__(self, checkpointName, opStr, out_path_str):
        print("opStr(2nd arg) -> Normalize(N), Inverse Log2(I), Gamma(G), Histograms(H)")

        os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
        self.checkpointName = checkpointName
        ### TODO: Make this param dynamic (have to change everytime on train/test) --- DONE
        self.out_path = out_path_str
        
        # Validation 
        self.normalize_bool = False
        self.inverse_tm_bool = False
        self.gamma_tm_bool = False
        self.hist_bool = False

        self.opStr = opStr
        # Control flow
        self.control_flow()

    def saveImage(self, filename, image):
        cv.imwrite(filename, image.astype(np.float32), [cv.IMWRITE_EXR_TYPE, cv.IMWRITE_EXR_TYPE_HALF])  # type: ignore

    def loadImage(self, filename, imreadFlags=None):
        return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))

    def plot_histograms(self):
        # split the image into its channels
        path = self.out_path 
        
        # remove all files that contain "hist" in their name from the path mentioned above
        for f in os.listdir(path):
            if "histogram" in f:
                os.remove(path + f)

        for f in os.listdir(path):
            if 'itmLG2' in f and not 'gamma' in f and 'synthesized' in f:
                img = self.loadImage(path + f)
                if img is None:
                    continue
                
                # print(f"max px-value: {np.amax(img)})")

                channels = cv.split(img)
                colors = ("b", "g", "r")

                plt.figure()
                plt.title("Color Histogram")
                plt.xlabel("Bins")
                plt.ylabel("# pixels")
                # plot the histogram for each channel
                for (chan, color) in zip(channels, colors):
                    hist,bins = np.histogram(chan.ravel(), bins=np.r_[0, np.inf]) 
                    plt.plot(hist, color = color)
                plt.savefig(path + f"histogram_{f[:-4]}.png", dpi = 300)
                plt.close()
        self.hist_bool = True

    def normalize_minMax(self, data):
        if data.ndim > 2: # Will go through this one --- ndim = 3
            for i in range(data.shape[-1]):
                data[:,:,i] = (data[:,:,i] - np.min(data[:,:,i])) / (np.max(data[:,:,i]) - np.min(data[:,:,i]))
        else: 
            data = (data - np.min(data)) / (np.max(data) - np.min(data))
        return data

    def normalize(self):
        for f in os.listdir(self.out_path):
            if '.exr' in f and not "N_" in f:
                # print(f)
                img = self.loadImage(self.out_path + f)
                img = self.normalize_minMax(img)
                self.saveImage(self.out_path + 'N_' + f, img)
        self.normalize_bool = True

    def inverse_tm(self):
        for f in os.listdir(self.out_path):
            if '.exr' in f and not "itmLG2" in f:
                # print(f)
                img = self.loadImage(self.out_path + f)
                img = tm.tm_model.tonemap_inv(img)
                self.saveImage(self.out_path + "itmLG2_" + f, img)
        self.inverse_tm_bool = True

    def gamma_tm(self):
        for f in os.listdir(self.out_path):
            if 'itmLG2' in f and not "gamma" in f:
                img = self.loadImage(self.out_path + f)
                img = tm.tm_display.tonemap(img)
                # img = np.clip(img, 0, 255) # Already happening in tonemap_display 
                cv.imwrite(self.out_path + "gamma_" + f[:-4] + ".png", img)
        self.gamma_tm_bool = True
    
    def reader(self):
        for f in os.listdir(self.out_path):
            print(f)

    def control_flow(self):
        # self.reader()
        if "N" in self.opStr:
            self.normalize()
            assert self.normalize_bool == True, "? Couldn't normalize"

        if "I" in self.opStr:
            self.inverse_tm()
            assert self.inverse_tm_bool == True, "? Couldn't inv-log TM"

        if "G" in self.opStr:
            self.gamma_tm()
            assert self.gamma_tm_bool == True, "? Couldn't Gamma TM"

        if "H" in self.opStr:
            self.plot_histograms()
            assert self.hist_bool == True, "? Couldn't plot histograms"
