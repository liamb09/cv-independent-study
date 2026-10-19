import numpy as np
import cv2
import math

sobel = (
    np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]),
    np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])
)

def to_greyscale (pixel_grid):
    new_grid = []

    for row in pixel_grid:
        new_grid.append([])
        for pixel in row:
            new_grid[-1].append(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])

    return np.array(new_grid)

def gaussian (pixel_grid, sigma):
    kernel_size = 2 * math.ceil(3*sigma) + 1
    variance = sigma ** 2

    hor_kernel = np.array([[0 for i in range(kernel_size)]]).astype(float)
    ver_kernel = np.array([[0] for i in range(kernel_size)]).astype(float)

    for i in range(kernel_size):
        val = math.e ** (-0.5 * ((i - math.floor(kernel_size/2))**2) / variance)
        hor_kernel[0][i] = val / (2 * math.pi * variance)
        ver_kernel[i][0] = val

    # print(hor_kernel, "\n", ver_kernel)
    
    blurred = cv2.filter2D(pixel_grid, -1, hor_kernel)
    blurred = cv2.filter2D(blurred, -1, ver_kernel)

    return blurred

def neighbors (grid, row, col):
    ret = []
    #             0         1        2        3        4       5        6       7
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dy, dx in directions:
        if 0 <= row+dy < len(grid) and 0 <= col+dx < len(grid[0]):
            ret.append(grid[row+dy][col+dx])
    
    return ret

def is_zero_crossing (pixel_grid, row, col):

    if row == 0 or row == pixel_grid.shape[0]-1 or col == 0 or col == pixel_grid.shape[1]-1:
        return False

    p = pixel_grid[row][col]
    n_p = neighbors(pixel_grid, row, col) # lb, l, lt, b, t, rb, r, rt

    for n in n_p:
        if n*p < 0:
            # print(n, p)
            return abs(n - p)
    
    return 0

def hysteresis_threshold (pixel_grid, high_threshold, low_threshold):
    ret = np.zeros(pixel_grid.shape)

    # identify certain edges (pixels whose brightness exceeds high_threshold)
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[0])):
            if pixel_grid[row][col] >= high_threshold:
                ret[row][col] = 1
            elif pixel_grid[row][col] >= low_threshold:
                ret[row][col] = 0.5

    # promote candidate edges that are neighbors with certain edges
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[0])):
            if ret[row][col] == 0.5:
                ret[row][col] = 1 if (1 in neighbors(pixel_grid, row, col)) else 0

    return ret * 255

def canny_ed (pixel_grid, sigma):

    pixel_grid = to_greyscale(pixel_grid)
    smoothed = gaussian(pixel_grid, sigma)

    # here, "I" represents the image, and the subscripts represent the direction of
    #   the partial derivative
    I_x = cv2.filter2D(smoothed, cv2.CV_64F, sobel[0])
    I_y = cv2.filter2D(smoothed, cv2.CV_64F, sobel[1])

    I_xx = cv2.filter2D(I_x, cv2.CV_64F, sobel[0])
    I_xy = cv2.filter2D(I_x, cv2.CV_64F, sobel[1])
    I_yy = cv2.filter2D(I_y, cv2.CV_64F, sobel[1])
    
    gradient_laplacian = [] # the laplacians at each point in the gradient direction
    for row in range(len(I_x)):
        gradient_laplacian.append([])
        for col in range(len(I_x[0])):
            norm_magnitude = math.sqrt(I_x[row][col]**2 + I_y[row][col]**2)
            if (abs(I_x[row][col]) < 0.000001 and abs(I_y[row][col]) < 0.000001) or norm_magnitude == 0:
                gradient_laplacian[-1].append(0)
            else:
                n_x = I_x[row][col] / norm_magnitude
                n_y = I_y[row][col] / norm_magnitude
                gradient_laplacian[-1].append(
                    n_x**2 * I_xx[row][col] + 
                    2*n_x*n_y * I_xy[row][col] +
                    n_y**2 * I_yy[row][col]
                )
    gradient_laplacian = np.array(gradient_laplacian)

    zero_crossing_probability = np.zeros(gradient_laplacian.shape)
    for row in range(len(gradient_laplacian)):
        for col in range(len(gradient_laplacian[0])):
            zero_crossing_probability[row][col] = is_zero_crossing(gradient_laplacian, row, col)

    high_threshold = 3
    low_threshold = 2

    edges = hysteresis_threshold(zero_crossing_probability, low_threshold, high_threshold)
    
    # gradient_laplacian = (gradient_laplacian - np.min(gradient_laplacian)) / (np.max(gradient_laplacian) - np.min(gradient_laplacian))*255
    # ret = np.zeros(gradient_laplacian.shape)
    # for row in range(len(gradient_laplacian)):
    #     for col in range(len(gradient_laplacian[0])):
    #         ret[row][col] = 255 if abs(gradient_laplacian[row][col] - 255*.4) < 30 else 0

    return edges