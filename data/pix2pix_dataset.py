"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""
import sys

from data.base_dataset import BaseDataset, get_params, get_transform
from PIL import Image
import util.tonemap as tm
import util.util as util
import os
import cv2 as cv
import numpy as np

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1" 

class Pix2pixDataset(BaseDataset):
    @staticmethod
    def modify_commandline_options(parser, is_train):
        parser.add_argument('--no_pairing_check', action='store_true',
                            help='If specified, skip sanity check of correct label-image file pairing')
        return parser

    def initialize(self, opt):
        self.opt = opt

        label_paths, image_paths, instance_paths = self.get_paths(opt)

        util.natural_sort(label_paths)
        util.natural_sort(image_paths)
        if not opt.no_instance:
            util.natural_sort(instance_paths)

        label_paths = label_paths[:opt.max_dataset_size]
        image_paths = image_paths[:opt.max_dataset_size]
        instance_paths = instance_paths[:opt.max_dataset_size]

        if not opt.no_pairing_check:
            for path1, path2 in zip(label_paths, image_paths):
                assert self.paths_match(path1, path2), \
                    "The label-image pair (%s, %s) do not look like the right pair because the filenames are quite different. Are you sure about the pairing? Please see data/pix2pix_dataset.py to see what is going on, and use --no_pairing_check to bypass this." % (path1, path2)

        self.label_paths = label_paths
        self.image_paths = image_paths
        self.instance_paths = instance_paths

        size = len(self.label_paths)
        self.dataset_size = size

    def get_paths(self, opt):
        label_paths = []
        image_paths = []
        instance_paths = []
        assert False, "A subclass of Pix2pixDataset must override self.get_paths(self, opt)"
        return label_paths, image_paths, instance_paths

    def paths_match(self, path1, path2):
        filename1_without_ext = os.path.splitext(os.path.basename(path1))[0]
        filename2_without_ext = os.path.splitext(os.path.basename(path2))[0]
        return filename1_without_ext == filename2_without_ext

    def loadImage(self, filename, imreadFlags=None):
        return cv.imread(filename, (cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH | cv.IMREAD_UNCHANGED))

    def saveImage(self, filename, image):
        cv.imwrite(filename, image.astype(np.float32), [cv.IMWRITE_EXR_TYPE, cv.IMWRITE_EXR_TYPE_HALF])  # type: ignore

    def __getitem__(self, index):
        # Label Image
        label_path = self.label_paths[index]
        # print(label_path)
        if ".exr" in label_path:
            label = self.loadImage(label_path)
            # print(f"label shape: {np.asarray(label).shape}")
            label = Image.fromarray(np.asarray(label))  # type: ignore
 
        else: # Goes through this... using png masks to conserve space!
            label = Image.open(label_path)
            # print(type(label))

        params = get_params(self.opt, label.size)
        
        # Params to transfer the same aug to image from label
        hflipB, vflipB = False, False
        rotation_angle = 0
        if self.opt.rand_rotate and not self.opt.no_flip: # train-time: Always rotate & flip! (2 augs so far)
            transform_label, rotation_angle, hflipB, vflipB = get_transform(self.opt, params, method=Image.NEAREST, normalize=False)
        elif self.opt.rand_rotate:
            transform_label, rotation_angle = get_transform(self.opt, params, method=Image.NEAREST, normalize=False)
        else: # test time
            transform_label = get_transform(self.opt, params, method=Image.NEAREST, normalize=False)
            

        label_tensor = transform_label(label) * 255.0
        label_tensor[label_tensor == 255] = self.opt.label_nc  # 'unknown' is opt.label_nc

        # input image (real images)
        image_path = self.image_paths[index]
        assert self.paths_match(label_path, image_path), \
            "The label_path %s and image_path %s don't match." % \
            (label_path, image_path)
        
        if ".exr" in image_path:
            image = self.loadImage(image_path)

            if not self.opt.tonemapped:
                # Expected images: skyangular linear space HDRs --- need to change dataset as well now.
                image = tm.tm_model.tonemap(image)
        else:
            image = Image.open(image_path)
        

        transform_image = get_transform(self.opt, params, isLabel=False, rotation_angle=rotation_angle, hflip_bool=hflipB, vflip_bool=vflipB)
        image_tensor = transform_image(image)
        # print(image_tensor.shape, image_tensor.dtype, image_tensor.device)
        # if using instance maps
        if self.opt.no_instance:
            instance_tensor = 0
        else:
            instance_path = self.instance_paths[index]

            if ".exr" in instance_path:
                instance = self.loadImage(instance_path)
                instance = Image.fromarray(np.asarray(instance_path))  # type: ignore
            else:
                instance = Image.open(instance_path)

            if instance.mode == 'L':
                instance_tensor = transform_label(instance) * 255
                instance_tensor = instance_tensor.long()
            else:
                instance_tensor = transform_label(instance)

        input_dict = {'label': label_tensor,
                      'instance': instance_tensor,
                      'image': image_tensor,
                      'path': image_path,
                      }
        
        # print(f"input_dict[image]: {input_dict['image']}")
        
        # Give subclasses a chance to modify the final output
        self.postprocess(input_dict)

        return input_dict

    def postprocess(self, input_dict):
        return input_dict

    def __len__(self):
        return self.dataset_size
