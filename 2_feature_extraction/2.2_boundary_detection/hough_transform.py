import sys
sys.path.insert(0, '../2.1_edge_detection/')

import canny_ed
import differential_ed
import math
import numpy as np
import cv2

def to_greyscale (pixel_grid):
    new_grid = []

    for row in pixel_grid:
        new_grid.append([])
        for pixel in row:
            new_grid[-1].append(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])

    return np.array(new_grid)

def fetch_window (pixel_grid, row, col, window_size):
    ret = []
    for i in range(window_size):
        for j in range(window_size):
            # exclude point at (row, col)
            if i == window_size//2 and j == window_size//2:
                break
            row_idx = row - window_size//2 + i
            col_idx = col - window_size//2 + j
            if 0 <= row_idx < len(pixel_grid) and 0 <= col_idx < len(pixel_grid[0]):
                ret.append(pixel_grid[row_idx][col_idx])
    return ret

def detect_lines (pixel_grid, use_laplacian=False):
    og_grid = pixel_grid.copy()
    if use_laplacian:
        edges = differential_ed.laplacian_ed(pixel_grid, 30, 100)
    else:
        edges = canny_ed.canny_ed(pixel_grid, 5)

    pixel_grid = to_greyscale(pixel_grid)

    img_h, img_w = pixel_grid.shape
    max_rho = math.floor(math.sqrt(img_w**2 + img_h**2))
    rho_interval = 5
    theta_interval = 0.04

    accumulator_array = np.zeros((math.floor(math.pi / theta_interval), math.floor(2*max_rho / rho_interval)))
    for row in range(len(edges)):
        for col in range(len(edges[row])):
            if edges[row][col] > 0:
                for i in range(len(accumulator_array)):
                    theta = i*theta_interval
                    vote = -(col*math.sin(theta) - row*math.cos(theta))
                    rho_index = round((vote + max_rho) / rho_interval)
                    accumulator_array[i][rho_index] += 1

    # threshold with non-maximal suppression
    window_size = 13
    thresholded_array = np.zeros(accumulator_array.shape)
    for i in range(len(accumulator_array)):
        for j in range(len(accumulator_array[i])):
            window = fetch_window(accumulator_array, i, j, window_size)
            if accumulator_array[i][j] >= max(window):
                thresholded_array[i][j] = accumulator_array[i][j]
    
    # thresholded_array = (thresholded_array - np.min(thresholded_array))/(np.max(thresholded_array) - np.min(thresholded_array))*255

    threshold = 0.5*np.max(thresholded_array)
    for i in range(len(thresholded_array)):
        for j in range(len(thresholded_array[i])):
            if thresholded_array[i][j] > threshold:
                rho = j*rho_interval - max_rho
                theta = i*theta_interval
                cv2.line(
                    og_grid,
                    (0, int(rho/math.cos(theta))),
                    (img_w-1, int(((img_w-1)*math.sin(theta) + rho)/math.cos(theta))),
                    (255, 0, 0),
                    2
                )

    return og_grid

def detect_circles (pixel_grid, radius, use_laplacian=False):
    og_grid = pixel_grid
    if use_laplacian:
        edges = differential_ed.laplacian_ed(pixel_grid, 30, 100)
    else:
        edges = canny_ed.canny_ed(pixel_grid, 5)

    pixel_grid = to_greyscale(pixel_grid)

    img_h, img_w = pixel_grid.shape
    interval = 5
    accumulator_array = np.zeros((math.floor(img_h/interval), math.floor(img_w/interval)))
    for row in range(len(edges)):
        for col in range(len(edges[row])):
            if edges[row][col] > 0:
                for i in range(radius*2):
                    x = i - radius
                    
                    y = row + math.sqrt(radius**2 - x**2)
                    if 0 <= round((x+col) / interval) < len(accumulator_array[0]) and 0 <= round((y+row) / interval) < len(accumulator_array):
                        accumulator_array[round((y+row) / interval)][round((x+col) / interval)] += 1

                    y = row - math.sqrt(radius**2 - x**2)
                    if 0 <= round((x+col) / interval) < len(accumulator_array[0]) and 0 <= round((y+row) / interval) < len(accumulator_array):
                        accumulator_array[round((y+row) / interval)][round((x+col) / interval)] += 1
    
    # threshold with non-maximal suppression
    thresholded_array = accumulator_array
    # window_size = 11
    # thresholded_array = np.zeros(accumulator_array.shape)
    # for i in range(len(accumulator_array)):
    #     for j in range(len(accumulator_array[i])):
    #         window = fetch_window(accumulator_array, i, j, window_size)
    #         if accumulator_array[i][j] >= max(window):
    #             thresholded_array[i][j] = accumulator_array[i][j]
    
    thresholded_array = (thresholded_array - np.min(thresholded_array))/(np.max(thresholded_array) - np.min(thresholded_array))*255

    threshold = 0.8*np.max(thresholded_array)
    for i in range(len(thresholded_array)):
        for j in range(len(thresholded_array[i])):
            if thresholded_array[i][j] > threshold:
                x = j * interval
                y = i * interval
                print(thresholded_array[i][j])
                cv2.circle(
                    og_grid,
                    (x, y),
                    radius,
                    (255, 0, 0),
                    2
                )

    return thresholded_array

# 180     : 90
# 170-177 : 88
# 212-215 : 107