## TODOs:  
~~0. Reduce dataset size ~100 samples (run for couple of epochs) --> sanity checks~~  
    ~~a. Fix Tonemapping - log2 -> model~~; gamma2.2 -> visualization (tonemap.py)  
    ~~b. 10-20 epochs should be coherent~~  
~~1. For Tensorboard (RGB -- in BGR right now) -- fix that~~   
~~2. Save images as exrs (use skymangler/core)~~  
~~3. Why is the skydome cropped? -- Never crop~~
~~4. Just random rotate and no other aug!~~ 
5. ffmpeg videos to see the results!   (P1) 
[Till Tom]  
--- (Retrain first) ---
~~6. Run test on current and new ones!   (P1)~~ 
7. Swap to dataset : laval_HDRdb :: SkynetSegmented_HDRdb (deepsky)  
~~8. Don't use 2014 samples --> Use 2016~~  
9. Get random images -> Validation exp. -> use radial skies from skymangler --> make the video.  
[Monday/Tuesday]
--- 
#### Thoughts:  
1. Masking the loss -> The buildings (if rand_rotate is on and buildings appear in the same place)  
2. Keep referencing Ian's pix2pix repo.
--- 
### Intel:
delta_0 -> Has a lot of renaming and tonemapping code in /web/images (extract and keep in utils)
---