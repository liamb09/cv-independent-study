import numpy as np
import cv2

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
    )
}

def edges (pixel_grid, kernel_name="sobel_3x3"):
    kernel_x, kernel_y = kernels[kernel_name]

    filtered = cv2.filter2D(pixel_grid, -1, kernel_x)
    filtered = cv2.filter2D(filtered, -1, kernel_y)

    return filtered