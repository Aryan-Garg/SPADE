# usage:
# ./export_test.sh <name> <movie_name>
echo "usage: ./export_test.sh <name> <movie_name>"

MASK="$1/input_label"
SPADE="$1/synthesized_image"

GAMMA_LABEL=1.0
GAMMA_IMAGE=2.2

/usr/bin/ffmpeg -y \
      -gamma $GAMMA_LABEL -framerate 1 -f image2 -start_number 1 -thread_queue_size 1024  -i "datasets/full_pysolar_dataset/full_test_discrete/masks_color/$2_%d.png" \
      -gamma $GAMMA_IMAGE -framerate 1 -f image2 -start_number 1 -thread_queue_size 1024  -i "datasets/full_pysolar_dataset/full_gt_test/$2_%d.exr" \
     \
      -vcodec libx265 -pix_fmt yuvj420p -crf 28 -preset ultrafast -filter_complex \
       "[0:v]drawtext=text='Mask':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v0]; \
        [1:v]drawtext=text='Synth':fontcolor=green:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=text_h:y=text_h[v1]; \
        [v0][v1]hstack=inputs=2[v]" \
      -map "[v]" \
      -r 1 \
      -f mov \
      "$2.mov"