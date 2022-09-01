#!/bin/bash

# VIDEO
# Usage: ./export_vid.sh
MASK_TYPE="results/val_masks_4/jimbo_full_100/test_latest/images/input_label"
SPADE_OUT="results/val_masks_4/jimbo_full_100/test_latest/images/synthesized_image"
REAL_OUT="datasets/validation/val_one_day"
GAMMA_LABEL=1.0
GAMMA_IMAGE=2.2
/usr/bin/ffmpeg -y \
      -gamma $GAMMA_LABEL -framerate 1 -f image2 -start_number 1 -thread_queue_size 1024  -i "$MASK_TYPE/20160521_%d.png" \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -start_number 1 -thread_queue_size 1024  -i "$REAL_OUT/r_20160521_%d.exr" \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -start_number 1 -thread_queue_size 1024  -i "$SPADE_OUT/itmLG2_20160521_%d.exr" \
     \
      -vcodec libx264 -pix_fmt yuvj420p -crf 20 -preset ultrafast -filter_complex \
       "[0:v]drawtext=text='Mask':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v0]; \
        [1:v]drawtext=text='Real':fontcolor=green:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v1]; \
        [2:v]drawtext=text='SPADE':fontcolor=red:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v2]; \
        [v0][v1][v2]hstack=inputs=3[v]" \
      -map "[v]" \
      -r 1 \
      -f mov \
      "one_full_day.mov"