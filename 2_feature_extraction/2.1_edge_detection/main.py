from PIL import Image
import numpy as np
import sys
import gradient_ed

def to_greyscale (pixel_grid):
    new_grid = []

    for row in pixel_grid:
        new_grid.append([])
        for pixel in row:
            new_grid[-1].append(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])

    return np.array(new_grid)
                 

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
# pixel_grid = to_greyscale(pixel_grid)

edges = gradient_ed.edges(pixel_grid, "prewitt")

newimg = Image.fromarray(edges.astype(np.uint8))
newimg.save(dest_path)