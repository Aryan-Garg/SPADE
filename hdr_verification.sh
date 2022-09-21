#!/bin/bash

# VIDEO
# Usage: ./export_vid.sh
PATH="checkpoints/hdr_verification"
FIRST="10"
SECOND="100"

GAMMA_LABEL=1.0
GAMMA_IMAGE=2.2
/usr/bin/ffmpeg -y \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "checkpoints/jimbo_full_100/web/images/real/itmLG2_*.exr" \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$PATH/div$FIRST_*" \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$PATH/div$SECOND_*" \
     \
      -vcodec libx264 -pix_fmt yuvj420p -crf 20 -preset ultrafast -filter_complex \
       "[0:v]drawtext=text='REAL':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v0]; \
        [1:v]drawtext=text='DIV:$FIRST':fontcolor=green:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v1]; \
        [2:v]drawtext=text='DIV:$SECOND':fontcolor=red:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v2]; \
        [v0][v1][v2]hstack=inputs=3[v]" \
      -map "[v]" \
      -r 1 \
      -f mov \
      "div_10_100.mov"