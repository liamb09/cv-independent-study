import math

def avg_pixel_value (pixel_grid):
    pixel_sum = (0,0,0)

    for row in pixel_grid:
        for col in row:
            pixel_sum += col
    
    return pixel_sum / (len(pixel_grid) * len(pixel_grid[0]))

def apply_1d_kernel (pixel_grid, kernel)

def gaussian (pixel_grid, kernel_size):
    sigma = kernel_size / (2*math.pi) # standard deviation
    variance = sigma ** 2

    avg_pixel = avg_pixel_value(pixel_grid)

    return pixel_grid