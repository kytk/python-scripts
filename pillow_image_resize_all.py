#!/usr/bin/python3

import os
import glob
from PIL import Image

dst_dir = './images_magnified'
os.makedirs(dst_dir, exist_ok=True)

files = glob.glob('./*.png')

for f in files:
    img = Image.open(f)
    img_resize = img.resize((img.width * 4, img.height * 4), Image.LANCZOS)
    root, ext = os.path.splitext(f)
    basename = os.path.basename(root)
    img_resize.save(os.path.join(dst_dir, basename + '_m' + ext))
