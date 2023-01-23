"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

import os
from collections import OrderedDict
from tqdm.auto import tqdm

import data
from options.test_options import TestOptions

from models.pix2pix_model import Pix2PixModel
from util.visualizer import Visualizer
from util import html

# Aryan's custom imports
from util.postprocess import PostProcessor 
import torch 

opt = TestOptions().parse()

dataloader = data.create_dataloader(opt)

model = Pix2PixModel(opt)
model.eval()

visualizer = Visualizer(opt)

# create a webpage that summarizes the all results
web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' %
                    (opt.name, opt.phase, opt.which_epoch))

for i, data_i in enumerate(tqdm(dataloader)):
    if i * opt.batchSize >= opt.how_many:
        break

    generated = model(data_i, mode='inference')
    img_path = data_i['path']

    for b in range(generated.shape[0]):
        visuals = OrderedDict([('input_label', data_i['label'][b]),
                               ('synthesized_image', generated[b])])
        visualizer.save_images(webpage, visuals, img_path[b:b + 1])

webpage.save()

post_processor_inst = PostProcessor(opt.name, "I", f"{opt.results_dir}/{opt.name}/test_{opt.which_epoch}/images/synthesized_image/")
print(f"\nNormalization Stat: {post_processor_inst.normalize_bool}")
print(f"Inv-log2 TM Stat: {post_processor_inst.inverse_tm_bool}")
print(f"Gamma TM Stat: {post_processor_inst.gamma_tm_bool}")
print(f"Histogram Stat: {post_processor_inst.hist_bool}")

# call export_test.sh script to export video
os.system(f"./export_test.sh {opt.results_dir}/{opt.name}/test_{opt.which_epoch}/images/ {opt.results_dir[8:]}")