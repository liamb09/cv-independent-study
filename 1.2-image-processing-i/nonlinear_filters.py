import math
import numpy as np

def apply_kernel_to_point (pixel_grid, kernel, center_x, center_y):
    sum = np.array([0, 0, 0], dtype=np.float32)
    for row in range(len(kernel)):
        if not (0 <= center_y+row-len(kernel)//2 < len(pixel_grid)):
            continue
        for col in range(len(kernel[0])):
            if not (0 <= center_x+col-len(kernel[0])//2 < len(pixel_grid[0])):
                continue
            sum += pixel_grid[center_y+row-len(kernel)//2][center_x+col-len(kernel[0])//2] * kernel[row][col]
            
    return [min(i, 255) for i in sum]

def bilateral (pixel_grid, spatial_sigma, brightness_sigma):
    print(len(pixel_grid), len(pixel_grid[0]))
    kernel_size = 2*math.ceil(3*spatial_sigma) + 1
    # spatial_sigma = 3 #kernel_size / (2*math.pi) # standard deviation
    print(kernel_size)
    gaussian_variance = spatial_sigma ** 2

    # brightness_sigma = 30

    gaussian_kernel = np.zeros((kernel_size, kernel_size))

    for i in range(kernel_size):
        val1 = math.e ** (-0.5 * ((i - math.floor(kernel_size/2))**2) / gaussian_variance)
        for j in range(kernel_size):
            val2 = math.e ** (-0.5 * ((j - math.floor(kernel_size/2))**2) / gaussian_variance)
            gaussian_kernel[i, j] = val1*val2 / (2 * math.pi * gaussian_variance)

    print(gaussian_kernel)

    brightness_gaussian = lambda k:  math.exp(-0.5 * (k**2) / (brightness_sigma**2)) #1 / (math.sqrt(2*math.pi) * brightness_sigma)

    pixel_grid = pixel_grid.astype(np.float32)
    new_grid = pixel_grid.copy()
    brightness_gaussian_kernel = np.zeros((kernel_size, kernel_size))
    np.set_printoptions(suppress=True, precision=10)
    np.set_printoptions(linewidth=200)
    for row in range(len(pixel_grid)):
        print(row)
        for col in range(len(pixel_grid[row])):

            brightness_gaussian_kernel.fill(0)

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
                    if row == 150 and col == 100:
                        print(color_dist)
                        print(np.min(brightness_gaussian_kernel))
                        print(np.max(brightness_gaussian_kernel))
            
            
            bilateral_filter = np.multiply(gaussian_kernel, brightness_gaussian_kernel)
            bilateral_filter /= np.sum(bilateral_filter)

            # if row == 150 and col == 100:
            #     print(brightness_gaussian_kernel, "\n\n", bilateral_filter, "\n\n", np.sum(bilateral_filter))

            new_grid[row, col] = apply_kernel_to_point(pixel_grid, bilateral_filter, col, row)

    return new_grid