import numpy as np
import math

def compress_frame (pixel_grid, factor):
    height, width = pixel_grid.shape
    new_grid = np.zeros((math.ceil(height/factor), math.ceil(width/factor)))
    for row in range(0, len(pixel_grid), factor):
        for col in range(0, len(pixel_grid[0]), factor):
            pass

def lucas_kanade (frame1, frame2, initial_compression_factor):
    # initial_compression_factor is the factor by which to compress the frames for the first pass
    pass