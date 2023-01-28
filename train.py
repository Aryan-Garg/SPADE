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

from models.pix2pix_model import Pix2PixModel
from trainers.pix2pix_trainer import Pix2PixTrainer

# Aryan's Custom Imports
from util.postprocess import PostProcessor
import torch 

# parse options
opt = TrainOptions().parse()

# print options to help debugging
print(' '.join(sys.argv))

# load the training dataset
dataloader = data.create_dataloader(opt)
print(f"[+] Len(Training DataLoader): {len(dataloader)}")
# create trainer for our model
trainer = Pix2PixTrainer(opt)

# create tool for counting iterations
iter_counter = IterationCounter(opt, len(dataloader))

# create tool for visualization
visualizer = Visualizer(opt)

### Cheapest Workaround to get val loader 
# change paths to val dirs
opt.label_dir = f"datasets/full_pysolar_split80-10-10/full_discrete_val/masks"
opt.image_dir = f"datasets/full_pysolar_split80-10-10/full_val"
### 

val_dataloader = data.create_dataloader(opt)
print(f"[+] Len(Val DataLoader): {len(val_dataloader)}\n")

# def force_cudnn_initialization():
#     s = 32
#     dev = torch.device('cuda')
#     torch.nn.functional.conv2d(torch.zeros(s, s, s, s, device=dev), torch.zeros(s, s, s, s, device=dev))

# force_cudnn_initialization()
best_val_gLoss, best_val_dLoss = np.inf, np.inf

for epoch in tqdm(iter_counter.training_epochs()):
    iter_counter.record_epoch_start(epoch)
    for i, data_i in enumerate(dataloader, start=iter_counter.epoch_iter):
        iter_counter.record_one_iteration()

        # Training
        # train generator
        if i % opt.D_steps_per_G == 0:
            trainer.run_generator_one_step(data_i)

        # train discriminator
        trainer.run_discriminator_one_step(data_i)
  
        # Visualizations
        if iter_counter.needs_printing():
            losses = trainer.get_latest_losses()
            visualizer.print_current_errors(epoch, iter_counter.epoch_iter,
                                            losses, iter_counter.time_per_iter)
            visualizer.plot_current_errors(losses, iter_counter.total_steps_so_far)

        if iter_counter.needs_displaying():
            visuals = OrderedDict([('input_label', data_i['label']),
                                   ('synthesized_image', trainer.get_latest_generated()),
                                   ('real_image', data_i['image'])])
            # Set train flag to True to NOT save train images          
            visualizer.display_current_results(visuals, epoch, iter_counter.total_steps_so_far, train=True)

        # if iter_counter.needs_saving(): --- TODO: DON'T SAVE (DUMB) PERIODIC: DONE
        #     print('saving the latest model (epoch %d, total_steps %d)' %
        #           (epoch, iter_counter.total_steps_so_far))
        #     trainer.save('latest')
        #     iter_counter.record_current_iter()

    trainer.update_learning_rate(epoch)
    iter_counter.record_epoch_end()

    # TODO: Add Validation code here! --- DONE
    total_val_gLoss, total_val_dLoss = 0., 0.
    for i, data_i in enumerate(val_dataloader):

        gen, g_losses, d_losses = trainer.run_val_step(data_i)
        losses_dict = {**g_losses, **d_losses}

        # For tensorboard
        if (i+1) % opt.print_freq == 0:
            visualizer.print_current_errors(epoch, i+1, losses_dict, iter_counter.time_per_iter, val=True)
            visualizer.plot_current_errors(losses_dict, i+1, val=True)
        
        val_g_loss = sum(g_losses.values()).mean()
        val_d_loss = sum(d_losses.values()).mean()

        total_val_gLoss = total_val_gLoss + val_g_loss
        total_val_dLoss = total_val_dLoss + val_d_loss

    # Get per epoch validation losses
    total_val_gLoss = total_val_gLoss / len(val_dataloader)
    total_val_dLoss = total_val_dLoss / len(val_dataloader)
    
    # print(f"Epoch: {epoch} | Val. G_Loss : {total_val_gLoss} | Val. D_Loss : {total_val_dLoss}")
    
    # If best val error > this_epoch's val error: SAVE + Periodic saving
    if (best_val_gLoss > total_val_gLoss and best_val_dLoss > total_val_dLoss) or \
        epoch % opt.save_epoch_freq == 0 or \
        epoch == iter_counter.total_epochs:
        
        # Update best val results
        best_val_gLoss = total_val_gLoss
        best_val_dLoss = total_val_dLoss

        print('saving the model at the end of epoch %d, iters %d' %
              (epoch, iter_counter.total_steps_so_far))
        trainer.save('latest')
        trainer.save(epoch)

print('Training was successfully finished.')
# print('Inverse-log2 and gamma TMing now...')

# # Options: N/I/G/H
# post_processor_inst = PostProcessor(opt.name, "I", f"checkpoints/{opt.name}/web/images/")
# print(f"\nNormalization Stat: {post_processor_inst.normalize_bool}")
# print(f"Inv-log2 TM Stat: {post_processor_inst.inverse_tm_bool}")
# print(f"Gamma TM Stat: {post_processor_inst.gamma_tm_bool}")
# print(f"Histogram Plots Stat: {post_processor_inst.hist_bool}")

# # run separator.py file
# os.system(f"python separator.py {opt.name}")

# run export_train.sh script --- Don't need training movie
# os.system(f"./export_train.sh {opt.name}")