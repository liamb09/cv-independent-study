from PIL import Image
import numpy as np
import sys
import math

def convolution_via_fourier (pixel_grid, kernel):
    pass

if len(sys.argv) > 2:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
else:
    sys.exit("Please add command line arguments for source and destination image paths.")

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

row = []
for i in range(600):
    row.append([255*(math.sin(0.02 * math.pi * i) + 1)/2]*3)
pixel_grid = np.array([row]*600)

newimg = Image.fromarray(pixel_grid.astype(np.uint8))
newimg.save(dest_path)