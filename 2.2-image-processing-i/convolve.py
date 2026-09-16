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

# pixel_grid = kernels.gaussian(pixel_grid, 10)

pixel_grid = kernels.apply_kernel_to_grid(pixel_grid, [[0.000453939978252691, 0.004849689877341308, 0.010681177840860335, 0.004849689877341308, 0.000453939978252691], [0.004849689877341308, 0.05181189812124092, 0.11411288393741639, 0.05181189812124092, 0.004849689877341308], [0.010681177840860335, 0.11411288393741639, 0.2513274122874845, 0.11411288393741639, 0.010681177840860335], [0.004849689877341308, 0.05181189812124092, 0.11411288393741639, 0.05181189812124092, 0.004849689877341308], [0.000453939978252691, 0.004849689877341308, 0.010681177840860335, 0.004849689877341308, 0.000453939978252691]])

# pixel_grid = kernels.gaussian(pixel_grid, 5)

newimg = Image.fromarray(pixel_grid)
newimg.save(dest_path)