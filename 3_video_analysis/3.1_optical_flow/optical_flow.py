import numpy as np
import math
from PIL import Image

def compress_frame (pixel_grid, factor):
    height, width = pixel_grid.shape
    new_grid = np.zeros((math.ceil(height/factor), math.ceil(width/factor)))
    for row in range(0, len(pixel_grid), factor):
        for col in range(0, len(pixel_grid[0]), factor):
            sum = 0
            num_pixels = factor*factor
            for i in range(factor):
                if row+i >= len(pixel_grid):
                    num_pixels -= factor
                    continue
                for j in range(factor):
                    if col+j >= len(pixel_grid[0]):
                        num_pixels -= 1
                        continue
                    sum += pixel_grid[row+i][col+j]
            new_grid[row//factor][col//factor] = sum / num_pixels
    return new_grid

def lucas_kanade (frame1, frame2, initial_compression_factor=32):
    # initial_compression_factor is the factor by which to compress the frames for the first pass
    frame1_compressed = compress_frame(frame1, initial_compression_factor)
    newimg = Image.fromarray(frame1_compressed.astype(np.uint8))
    newimg.save("compressed_frame1.bmp")
    frame2_compressed = compress_frame(frame2, initial_compression_factor)
    newimg = Image.fromarray(frame2_compressed.astype(np.uint8))
    newimg.save("compressed_frame2.bmp")