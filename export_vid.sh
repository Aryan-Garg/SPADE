#!/bin/bash 

# MASK_TYPE="discrete"
# MASK_TYPE="clear_mask"
# SPADE_OUT="synth"
# REAL_OUT="real"
# DIFF="diff"
# # VIDEO
# GAMMA_LABEL=1.0
# GAMMA_IMAGE=1.0
# /usr/bin/ffmpeg -y \
#       -gamma $GAMMA_LABEL -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$MASK_TYPE/*.png" \
#       -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$REAL_OUT/*.exr" \
#       -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$SPADE_OUT/*.exr" \
#       -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$DIFF/*.exr" \
#      \
#       -vcodec libx264 -pix_fmt yuvj420p -crf 20 -preset ultrafast -filter_complex \
#        "[0:v]drawtext=text='Mask':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v0]; \
#         [1:v]drawtext=text='HDRdb':fontcolor=green:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v1]; \
#         [2:v]drawtext=text='SPADE':fontcolor=blue:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v2]; \
#         [3:v]drawtext=text='DIFF':fontcolor=red:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v3]; \
#         [v0][v1][v2][v3]hstack=inputs=4[v]" \
#       -map "[v]" \
#       -r 1 \
#       -f mov \
#       "HDRdb_SPADE_DIFF.mov"

# VIDEO
# Usage: ./export_vid.sh experiment_name
MASK_TYPE="checkpoints/$1/web/images/masks"
SPADE_OUT="checkpoints/$1/web/images/synth"
REAL_OUT="checkpoints/$1/web/images/real"
GAMMA_LABEL=1.0
GAMMA_IMAGE=2.2
/usr/bin/ffmpeg -y \
      -gamma $GAMMA_LABEL -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$MASK_TYPE/*.png" \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$REAL_OUT/*.exr" \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -pattern_type glob -thread_queue_size 1024  -i "$SPADE_OUT/*.exr" \
     \
      -vcodec libx264 -pix_fmt yuvj420p -crf 20 -preset ultrafast -filter_complex \
       "[0:v]drawtext=text='Mask':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v0]; \
        [1:v]drawtext=text='Real':fontcolor=green:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v1]; \
        [2:v]drawtext=text='SPADE':fontcolor=red:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v2]; \
        [v0][v1][v2]hstack=inputs=3[v]" \
      -map "[v]" \
      -r 1 \
      -f mov \
      "$1.mov"