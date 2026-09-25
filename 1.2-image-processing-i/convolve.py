from PIL import Image
import numpy as np
import sys
import linear_filters
import nonlinear_filters

if len(sys.argv) > 2:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
else:
    sys.exit("Please add command line arguments for source and destination image paths.")

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

# edge_detection_kernel = np.array([
#     [0, 1, 0],
#     [1, -4, 1],
#     [0, 1, 0]
# ]) / 8

# pixel_grid = linear_filters.gaussian(pixel_grid, 13)

pixel_grid = nonlinear_filters.bilateral(pixel_grid, 2, 50)

newimg = Image.fromarray(pixel_grid.astype(np.uint8))
newimg.save(dest_path)