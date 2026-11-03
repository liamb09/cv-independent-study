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

def detect_lines (pixel_grid, use_laplacian=False):
    og_grid = pixel_grid
    if use_laplacian:
        edges = differential_ed.laplacian_ed(pixel_grid, 30, 100)
    else:
        edges = canny_ed.canny_ed(pixel_grid, 5)

    pixel_grid = to_greyscale(pixel_grid)

    img_w, img_h = pixel_grid.shape
    max_rho = math.floor(math.sqrt(img_w**2 + img_h**2))
    rho_interval = 5
    theta_interval = 0.05

    accumulator_array = np.zeros((math.floor(math.pi / theta_interval), math.floor(2*max_rho / rho_interval)))
    for row in range(len(edges)):
        for col in range(len(edges[row])):
            if edges[row][col] > 0:
                for i in range(len(accumulator_array)):
                    theta = i*theta_interval
                    vote = col*math.sin(theta) - row*math.cos(theta)
                    rho_index = round((vote + max_rho) / rho_interval)
                    accumulator_array[i][rho_index] += 1
    threshold = 0.5*np.max(accumulator_array)
    for i in range(len(accumulator_array)):
        for j in range(len(accumulator_array[i])):
            if accumulator_array[i][j] > threshold:
                rho = j*rho_interval - max_rho
                theta = i*theta_interval
                # print(accumulator_array[i][j], theta, rho)
                cv2.line(
                    og_grid,
                    (0, int(rho/math.cos(theta))),
                    (img_w-1, int(((img_w-1)*math.sin(theta) + rho)/math.cos(theta))),
                    (255, 0, 0),
                    2
                )

    return og_grid