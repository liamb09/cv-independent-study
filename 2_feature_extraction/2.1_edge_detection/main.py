from PIL import Image
import numpy as np
import sys
import differential_ed
import canny_ed

if len(sys.argv) > 2:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
elif len(sys.argv) > 1:
    src_path = sys.argv[1]
    dest_path = "edges.jpg"
else:
    sys.exit("Please add command line arguments for source and destination image paths.")

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

edges = canny_ed.canny_ed(pixel_grid, 2)

newimg = Image.fromarray(edges.astype(np.uint8))
newimg.save(dest_path)