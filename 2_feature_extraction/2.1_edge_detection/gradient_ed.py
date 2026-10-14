import numpy as np
import cv2

def to_greyscale (pixel_grid):
    new_grid = []

    for row in pixel_grid:
        new_grid.append([])
        for pixel in row:
            new_grid[-1].append(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])

    return np.array(new_grid)

def neighbors (grid, row, col):
    ret = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (-1, 1), (-1, 0), (-1, 1)]
    
    for dy, dx in directions:
        if 0 <= row+dy < len(grid) and 0 <= col+dx < len(grid[0]):
            ret.append(grid[row+dy][col+dx])
    
    return ret

kernels = {
    "prewitt": (
        np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ]),
        np.array([
            [1, 1, 1],
            [0, 0, 0],
            [-1, -1, -1]
        ])
    ),
    "sobel_3x3": (
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
    ),
    "sobel_5x5": (
        np.array([
            [-1, -2, 0, 2, 1],
            [-2, -3, 0, 3, 2],
            [-3, -5, 0, 5, 3],
            [-2, -3, 0, 3, 2],
            [-1, -2, 0, 2, 1]
        ]),
        np.array([
            [1, 2, 3, 2, 1],
            [2, 3, 5, 3, 2],
            [0, 0, 0, 0, 0],
            [-2, -3, -5, -3, -2],
            [-1, -2, -3, -2, -1]
        ])
    ),
    "scharr": (
        np.array([
            [-3, 0, 3],
            [-10, 0, 10],
            [-3, 0, 3]
        ]),
        np.array([
            [3, -10, -3],
            [0, 0, 0],
            [3, 10, 3]
        ])
    )
}

def edges (pixel_grid, l_thresh=60, h_thresh=160, kernel_name="sobel_3x3"):
    kernel_x, kernel_y = kernels[kernel_name]

    filtered = cv2.filter2D(pixel_grid, -1, kernel_x)
    filtered = to_greyscale(cv2.filter2D(filtered, -1, kernel_y))


    for row in range(len(filtered)):
        for col in range(len(filtered[row])):
            if filtered[row][col] >= h_thresh:
                filtered[row][col] = 1
            elif filtered[row][col] >= l_thresh:
                filtered[row][col] = 0.5
            else:
                filtered[row][col] = 0
    
    for row in range(len(filtered)):
        for col in range(len(filtered[row])):
            if filtered[row][col] == 0.5:
                if 1 in neighbors(filtered, row, col):
                    filtered[row][col] = 1
                else:
                    filtered[row][col] = 0
    
    filtered *= 255

    return filtered