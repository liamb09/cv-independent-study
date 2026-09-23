import math
import cv2
import numpy as np

def apply_kernel_to_point (pixel_grid, kernel, center_x, center_y):
    sum = np.array([0, 0, 0], dtype=np.float32)
    for row in range(len(kernel)):
        if center_y+row < 0 or center_y+row >= len(pixel_grid):
            continue
        for col in range(len(kernel[0])):
            if center_x+col < 0 or center_x+col >= len(pixel_grid[0]):
                continue
            sum += pixel_grid[center_y+row-math.floor(len(kernel)/2)][center_x+col-math.floor(len(kernel[0])/2)] * kernel[row][col]
            # if center_y == 1 and center_x == 1:
            #     print(pixel_grid[center_y+row][center_x+col], kernel[row][col])
            #     print("       ", sum)
    # if center_y == 1 and center_x == 1:
        # print(sum)
    return [min(i, 255) for i in sum]

def bilateral (pixel_grid, kernel_size):
    print(len(pixel_grid), len(pixel_grid[0]))
    gaussian_sigma = kernel_size / (2*math.pi) # standard deviation
    gaussian_variance = gaussian_sigma ** 2

    brightness_sigma = 10

    gaussian_kernel = np.zeros((kernel_size, kernel_size))

    for i in range(kernel_size):
        val1 = math.e ** (-0.5 * ((i - math.floor(kernel_size/2))**2) / gaussian_variance)
        for j in range(kernel_size):
            val2 = math.e ** (-0.5 * ((j - math.floor(kernel_size/2))**2) / gaussian_variance)
            gaussian_kernel[i, j] = val1*val2 / (2 * math.pi * gaussian_variance)
    

    brightness_gaussian = lambda k: 1 / (math.sqrt(2*math.pi) * brightness_sigma) * math.exp(-0.5 * (k**2) / (brightness_sigma**2))

    new_grid = pixel_grid.copy()
    brightness_gaussian_kernel = np.zeros((kernel_size, kernel_size))
    np.set_printoptions(suppress=True, precision=10)
    np.set_printoptions(linewidth=200)
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):

            # compute brightness gaussian
            for i in range(kernel_size):
                if not (0 <= row+i-math.floor(kernel_size/2) < len(pixel_grid)):
                    continue
                for j in range(kernel_size):
                    if not (0 <= col+j-math.floor(kernel_size/2) < len(pixel_grid[0])):
                        continue
                    
                    color_diff = pixel_grid[row, col] - pixel_grid[row+i-math.floor(kernel_size/2), col+j-math.floor(kernel_size/2)]
                    color_dist = math.sqrt(int(color_diff[0])**2 + int(color_diff[1])**2 + int(color_diff[2])**2)
                    
                    brightness_gaussian_kernel[i, j] = brightness_gaussian(color_dist)
            
            
            bilateral_filter = np.multiply(gaussian_kernel, brightness_gaussian_kernel)
            bilateral_filter /= np.sum(bilateral_filter)

            if row == 150 and col == 100:
                print(brightness_gaussian_kernel, "\n\n", bilateral_filter, "\n\n", np.sum(bilateral_filter))

            new_grid[row, col] = apply_kernel_to_point(pixel_grid, bilateral_filter, col, row)

    return new_grid