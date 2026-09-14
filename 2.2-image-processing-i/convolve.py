from PIL import Image
import numpy as np
import sys
import kernels

if len(sys.argv) > 2:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
else:
    sys.exit("Please add command line arguments for source and destination image paths.")

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

pixel_grid = kernels.gaussian(pixel_grid, 10)

newimg = Image.fromarray(pixel_grid)
newimg.save(dest_path)