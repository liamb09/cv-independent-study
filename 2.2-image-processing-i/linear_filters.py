import math
import cv2
import numpy as np

def apply_kernel_to_point (pixel_grid, kernel, center_x, center_y):
    sum = np.array([0, 0, 0], dtype=np.float32)
    for row in range(len(kernel)):
        if center_y+row-math.floor(len(kernel)/2) < 0 or center_y+row-math.floor(len(kernel)/2) >= len(pixel_grid):
            continue
        for col in range(len(kernel[0])):
            if center_x+col-math.floor(len(kernel[0])/2) < 0 or center_x+col-math.floor(len(kernel[0])/2) >= len(pixel_grid[0]):
                continue
            sum += pixel_grid[center_y+row-math.floor(len(kernel)/2)][center_x+col-math.floor(len(kernel[0])/2)] * kernel[row][col]
            # if center_y == 1 and center_x == 1:
            #     print(pixel_grid[center_y+row][center_x+col], kernel[row][col])
            #     print("       ", sum)
    # if center_y == 1 and center_x == 1:
        # print(sum)
    return [min(i, 255) for i in sum]

def apply_kernel_to_grid (pixel_grid, kernel):
    new_grid = pixel_grid.copy()
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            new_grid[row, col] = apply_kernel_to_point(pixel_grid, kernel, col, row)
    return new_grid

def gaussian (pixel_grid, kernel_size):
    sigma = kernel_size / (2*math.pi) # standard deviation
    variance = sigma ** 2

    hor_kernel = [[0 for i in range(kernel_size)]]
    ver_kernel = [[0] for i in range(kernel_size)]

    # print(hor_kernel, "\n", ver_kernel)

    for i in range(kernel_size):
        val = math.e ** (-0.5 * ((i - math.floor(kernel_size/2))**2) / variance)
        # print(val)
        hor_kernel[0][i] = val / (2 * math.pi * variance)
        ver_kernel[i][0] = val
    
    hor_kernel = np.array(hor_kernel, dtype=np.float32)
    ver_kernel = np.array(ver_kernel, dtype=np.float32)
    # print(hor_kernel, "\n", ver_kernel)
    
    pixel_grid = apply_kernel_to_grid(pixel_grid, hor_kernel)
    pixel_grid = apply_kernel_to_grid(pixel_grid, ver_kernel)
    # pixel_grid = cv2.filter2D(pixel_grid, -1, hor_kernel)
    # pixel_grid = cv2.filter2D(pixel_grid, -1, ver_kernel)
    
    # pixel_grid = pixel_grid * 1 / (2 * math.pi * variance)

    # avg_pixel = avg_pixel_value(pixel_grid)

    return pixel_grid