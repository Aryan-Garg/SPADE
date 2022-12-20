"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

import os
from collections import OrderedDict

import data
from options.test_options import TestOptions

from models.pix2pix_model import Pix2PixModel
from util.visualizer import Visualizer
from util import html

# Aryan's custom imports
from util.postprocess import PostProcessor 
import torch 
import torchmetrics
from torchmetrics.functional import structural_similarity_index_measure
import fidScore.fid_score as FID

opt = TestOptions().parse()

dataloader = data.create_dataloader(opt)

model = Pix2PixModel(opt)
model.eval()

visualizer = Visualizer(opt)

# create a webpage that summarizes the all results
web_dir = os.path.join(opt.results_dir, opt.name,
                       '%s_%s' % (opt.phase, opt.which_epoch))
webpage = html.HTML(web_dir,                    'Experiment = %s, Phase = %s, Epoch = %s' %
                    (opt.name, opt.phase, opt.which_epoch))

# test
print("Processing Masks...")
SSIM_overall, L1_overall = 0., 0.

for i, data_i in enumerate(dataloader):
    if i * opt.batchSize >= opt.how_many:
        break

    generated = model(data_i, mode='inference')

    # print(generated.shape, generated.device)
    # print(data_i['image'].shape, data_i)
    img_path = data_i['path']

    # Eval Testing
    synImage = generated
    reImage = data_i['image']
    # Eval Testing
    ## Compute:
    SSIM_ = structural_similarity_index_measure(synImage, reImage).detach()
    L1_ = torch.nn.functional.l1_loss(synImage, reImage).detach()
    print(f"Batch {i} ::\nSSIM: {SSIM_} | L1: {L1_}")
    ## Accumulate
    SSIM_overall = SSIM_overall + SSIM_
    L1_overall = L1_overall + L1_

    for b in range(generated.shape[0]):
        visuals = OrderedDict([('input_label', data_i['label'][b]),
                               ('synthesized_image', generated[b])])
        visualizer.save_images(webpage, visuals, img_path[b:b + 1])

SSIM_overall = SSIM_overall/len(dataloader)
L1_overall = L1_overall/len(dataloader)

# Show on tensorboard
visualizer.plot_current_errors({'SSIM': SSIM_overall, 'L1': L1_overall}, 1)

webpage.save()
print(f"Testing Avg. Eval Metrics:\nSSIM: {SSIM_overall} | L1: {L1_overall}\n")

REAL_IMG_PATH=f"datasets/full_dataset/full_gt_test/"
FAKE_IMG_PATH=f"results/{opt.name}/test_latest/images/synthesized_image/"
fid_score = FID.compute(path=[REAL_IMG_PATH, FAKE_IMG_PATH])
print(f"FID Score: {fid_score}")

post_processor_inst = PostProcessor(opt.name, "I", f"{opt.results_dir}/{opt.name}/test_{opt.which_epoch}/images/synthesized_image/")
print(f"\nNormalization Stat: {post_processor_inst.normalize_bool}")
print(f"Inv-log2 TM Stat: {post_processor_inst.inverse_tm_bool}")
print(f"Gamma TM Stat: {post_processor_inst.gamma_tm_bool}")
print(f"Histogram Stat: {post_processor_inst.hist_bool}")

call export_test.sh script to export video
os.system(f"./export_test.sh {opt.results_dir}/{opt.name}/test_{opt.which_epoch}/images/ {opt.results_dir[8:]}")