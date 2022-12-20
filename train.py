"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""
from tqdm.auto import tqdm
import numpy as np

import sys
import os
from collections import OrderedDict
from options.train_options import TrainOptions

import data
from util.iter_counter import IterationCounter
from util.visualizer import Visualizer

# Aryan's Custom Imports
from util.postprocess import PostProcessor 
import fidScore.fid_score as FID

from trainers.pix2pix_trainer import Pix2PixTrainer

import torch 
import torchmetrics
from torchmetrics.functional import structural_similarity_index_measure
import fidScore.fid_score as FID
# parse options
opt = TrainOptions().parse()

# print options to help debugging
print(' '.join(sys.argv))

# load the dataset
dataloader = data.create_dataloader(opt)
print(f"[+] Len(DataLoader): {len(dataloader)}\n")

# create trainer for our model
trainer = Pix2PixTrainer(opt)

# create tool for counting iterations
iter_counter = IterationCounter(opt, len(dataloader))

# create tool for visualization
visualizer = Visualizer(opt)

# def force_cudnn_initialization():
#     s = 32
#     dev = torch.device('cuda')
#     torch.nn.functional.conv2d(torch.zeros(s, s, s, s, device=dev), torch.zeros(s, s, s, s, device=dev))

# force_cudnn_initialization()
eval_dict = {'SSIM': [], 'L1': []}
for epoch in tqdm(iter_counter.training_epochs()):
    iter_counter.record_epoch_start(epoch)
    ssim_perEpoch, l1_perEpoch = 0., 0.
    for i, data_i in enumerate(dataloader, start=iter_counter.epoch_iter):
        iter_counter.record_one_iteration()

        # Training
        # train generator
        if i % opt.D_steps_per_G == 0:
            trainer.run_generator_one_step(data_i)

        # train discriminator
        trainer.run_discriminator_one_step(data_i)
        #
        synImage = trainer.get_latest_generated()
        # print(synImage.device, synImage.shape, synImage.dtype)
        reImage = data_i['image'].to(device=synImage.device)
        
        # Eval Training
        ## Compute:
        currSSIM = structural_similarity_index_measure(synImage, reImage).detach()
        currL1 = torch.nn.functional.l1_loss(synImage, reImage).detach()
        ## Accumulate:
        ssim_perEpoch = ssim_perEpoch + currSSIM
        l1_perEpoch = l1_perEpoch + currL1
        
        # Visualizations
        if iter_counter.needs_printing():
            losses = trainer.get_latest_losses()
            pass_eval_dict = {i:torch.Tensor(x) for i,x in eval_dict.items()}
            visualizer.print_current_errors(epoch, iter_counter.epoch_iter,
                                            dict(losses, **pass_eval_dict), iter_counter.time_per_iter)
            visualizer.plot_current_errors(dict(losses, **pass_eval_dict), iter_counter.total_steps_so_far)

        if iter_counter.needs_displaying():
            visuals = OrderedDict([('input_label', data_i['label']),
                                   ('synthesized_image', trainer.get_latest_generated()),
                                   ('real_image', data_i['image'])])
            # TODO:
            # A. Either use train lag to not save train images OR 
            # B. set flag --use_html to false                  
            visualizer.display_current_results(visuals, epoch, iter_counter.total_steps_so_far, train=True)

        if iter_counter.needs_saving():
            print('saving the latest model (epoch %d, total_steps %d)' %
                  (epoch, iter_counter.total_steps_so_far))
            trainer.save('latest')
            iter_counter.record_current_iter()

    trainer.update_learning_rate(epoch)
    iter_counter.record_epoch_end()
    
    # Evaluation: Divide by len of dataloader
    ssim_perEpoch = ssim_perEpoch / len(dataloader)
    l1_perEpoch = l1_perEpoch / len(dataloader)
    ## Save to Dict (for tensorboard vis.):
    eval_dict['SSIM'].append(ssim_perEpoch)
    eval_dict['L1'].append(l1_perEpoch)

    print("\n[~] Training (Avg.) Eval Metrics:")
    print(f"SSIM: {ssim_perEpoch} | L1: {l1_perEpoch}")

    if epoch % opt.save_epoch_freq == 0 or \
       epoch == iter_counter.total_epochs:
        print('saving the model at the end of epoch %d, iters %d' %
              (epoch, iter_counter.total_steps_so_far))
        trainer.save('latest')
        trainer.save(epoch)

print('Training was successfully finished.\n\nInverse-log2 and gamma TMing now...')

# Options: N/I/G/H
post_processor_inst = PostProcessor(opt.name, "I", f"checkpoints/{opt.name}/web/images/")
print(f"\nNormalization Stat: {post_processor_inst.normalize_bool}")
print(f"Inv-log2 TM Stat: {post_processor_inst.inverse_tm_bool}")
print(f"Gamma TM Stat: {post_processor_inst.gamma_tm_bool}")
print(f"Histogram Plots Stat: {post_processor_inst.hist_bool}")

# run separator.py file
os.system(f"python separator.py {opt.name}")

REAL_IMG_PATH=f"checkpoints/{opt.name}/web/images/real"
FAKE_IMG_PATH=f"checkpoints/{opt.name}/web/images/synth"
fid_score = FID.compute(path=[REAL_IMG_PATH, FAKE_IMG_PATH])
print(f"FID Score: {fid_score}")

# run export_train.sh script --- Don't need training movie
# os.system(f"./export_train.sh {opt.name}")