"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

import torch.utils.data as data
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import random
# import torchvision.transforms.functional as func_transforms

class BaseDataset(data.Dataset):
    def __init__(self):
        super(BaseDataset, self).__init__()

    @staticmethod
    def modify_commandline_options(parser, is_train):
        return parser

    def initialize(self, opt):
        pass


def get_params(opt, size):
    w, h = size
    new_h = h
    new_w = w
    if opt.preprocess_mode == 'resize_and_crop':
        new_h = new_w = opt.load_size
    elif opt.preprocess_mode == 'scale_width_and_crop':
        new_w = opt.load_size
        new_h = opt.load_size * h // w
    elif opt.preprocess_mode == 'scale_shortside_and_crop':
        ss, ls = min(w, h), max(w, h)  # shortside and longside
        width_is_shorter = w == ss
        ls = int(opt.load_size * ls / ss)
        new_w, new_h = (ss, ls) if width_is_shorter else (ls, ss)

    x = random.randint(0, np.maximum(0, new_w - opt.crop_size)) # type: ignore
    y = random.randint(0, np.maximum(0, new_h - opt.crop_size)) # type: ignore

    flip = random.random() > 0.5
    return {'crop_pos': (x, y), 'flip': flip}

### TODO: Change PIL transforms to torch transforms! 
### Upgrade to HDR capabilities
def get_transform(opt, params, method=Image.BICUBIC, normalize=False, toTensor=True, isLabel=True, rotation_angle=0, hflip_bool=False, vflip_bool=False):
    transform_list = []
    # First make a tensor; then do operations: rand_rotate -> resize(redundant)
    if toTensor: 
        transform_list += [transforms.ToTensor()]
        # print(transform_list)

    if opt.rand_rotate:
        if isLabel:
            rand_rotate = np.random.randint(0,360)
            # transform_list.append(transforms.Lambda(lambda img: __rand_rotate(img, rand_rotate)))
            transform_list.append(transforms.Lambda(lambda img: transforms.functional.rotate(img, rand_rotate))) # type: ignore
        else:
            # transform_list.append(transforms.Lambda(lambda img: __rand_rotate(img, rotation_angle)))
            transform_list.append(transforms.Lambda(lambda img: transforms.functional.rotate(img, rotation_angle))) # type: ignore

    if 'resize' in opt.preprocess_mode:
        osize = [opt.load_size, opt.load_size]
        transform_list.append(transforms.Resize(osize, interpolation=method)) # type: ignore
    elif 'scale_width' in opt.preprocess_mode:
        transform_list.append(transforms.Lambda(lambda img: __scale_width(img, opt.load_size, method)))
    elif 'scale_shortside' in opt.preprocess_mode:
        transform_list.append(transforms.Lambda(lambda img: __scale_shortside(img, opt.load_size, method)))

    if 'crop' in opt.preprocess_mode:
        transform_list.append(transforms.Lambda(lambda img: __crop(img, params['crop_pos'], opt.crop_size)))

    if opt.preprocess_mode == 'none':
        base = 32
        transform_list.append(transforms.Lambda(lambda img: __make_power_2(img, base, method)))
    
    if opt.preprocess_mode == 'fixed': 
        w = opt.crop_size
        h = round(opt.crop_size / opt.aspect_ratio)
        osize = [h, w]
        transform_list.append(transforms.Resize(osize, interpolation=transforms.InterpolationMode.BICUBIC))   
        # transform_list.append(transforms.Lambda(lambda img: __resize(img, w, h, method)))

    if opt.isTrain and not opt.no_flip:
        if isLabel:
            # Return these bools 
            hflip = bool(random.getrandbits(1)) # just get a fast random boolean val
            vflip = bool(random.getrandbits(1))
            if hflip:
                transform_list.append(transforms.Lambda(lambda img: transforms.functional.hflip(img)))
            if vflip:
                transform_list.append(transforms.Lambda(lambda img: transforms.functional.vflip(img)))
        else:
            if hflip_bool:
                transform_list.append(transforms.Lambda(lambda img: transforms.functional.hflip(img)))
            if vflip_bool:
                transform_list.append(transforms.Lambda(lambda img:transforms.functional.vflip(img)))
    if normalize:
        transform_list += [transforms.Normalize((0.5, 0.5, 0.5),
                                                (0.5, 0.5, 0.5))]

    # print(transform_list)
    if isLabel:
        if opt.rand_rotate and not opt.no_flip:
            return transforms.Compose(transform_list), rand_rotate, hflip, vflip # type: ignore
        elif opt.rand_rotate:
            return transforms.Compose(transform_list), rand_rotate
        else: # Pour l'heure de test ;)
            return transforms.Compose(transform_list)
    else:
        return transforms.Compose(transform_list)


def normalize():
    return transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))


def __resize(img, w, h, method=Image.BICUBIC):
    return img.resize((w, h), method)


def __make_power_2(img, base, method=Image.BICUBIC):
    ow, oh = img.size
    h = int(round(oh / base) * base)
    w = int(round(ow / base) * base)
    if (h == oh) and (w == ow):
        return img
    return img.resize((w, h), method)


def __scale_width(img, target_width, method=Image.BICUBIC):
    ow, oh = img.size
    if (ow == target_width):
        return img
    w = target_width
    h = int(target_width * oh / ow)
    return img.resize((w, h), method)


def __scale_shortside(img, target_width, method=Image.BICUBIC):
    ow, oh = img.size
    ss, ls = min(ow, oh), max(ow, oh)  # shortside and longside
    width_is_shorter = ow == ss
    if (ss == target_width):
        return img
    ls = int(target_width * ls / ss)
    nw, nh = (ss, ls) if width_is_shorter else (ls, ss)
    return img.resize((nw, nh), method)

def __crop(img, pos, size):
    ow, oh = img.size
    x1, y1 = pos
    tw = th = size
    return img.crop((x1, y1, x1 + tw, y1 + th))

def __flip(img, flip):
    if flip:
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    return img

def __rand_rotate(img, rand_rotate):
    return img.rotate(angle=rand_rotate)