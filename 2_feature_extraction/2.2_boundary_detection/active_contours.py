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

def find_gradient (pixel_grid):
    kernel_x, kernel_y, = (
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

    filtered = cv2.filter2D(pixel_grid, -1, kernel_x)
    filtered = to_greyscale(cv2.filter2D(filtered, -1, kernel_y))

    blurred = cv2.GaussianBlur(filtered, (5, 5), 0)

    return blurred

def uniformly_sample_contour (contour, num_points = None):
    if not num_points:
        num_points = len(contour)
    
    side_lengths = []
    cumulative_length = [0]
    for i in range(len(contour)):
        cur = contour[i]
        next = contour[(i+1) % len(contour)]
        side_lengths.append(math.sqrt((next[0] - cur[0])**2 + (next[1] - cur[1])**2))
        if i + 1 < len(contour):
            cumulative_length.append(cumulative_length[-1] + side_lengths[-1])
    
    separation_dist = sum(side_lengths) / num_points
    new_contour = [contour[0]]
    for i in range(1, num_points):
        cur_arclen = separation_dist * i
        start_point_idx = 0 # the point (on the old contour) just before this point on the new contour
        while i < len(cumulative_length) and cumulative_length[start_point_idx + 1] < cur_arclen:
            start_point_idx += 1
        
        leftover_arclen = cur_arclen - cumulative_length[start_point_idx]
        cur_sidelen = cumulative_length[start_point_idx+1] - cumulative_length[start_point_idx]
        new_contour.append((
            cumulative_length[start_point_idx+1]
        ))

    print(cumulative_length)

def find_next_point (point, pixel_grid, window_size):
    # returns point in surrounding window with minimum energy
    pass

def contour (pixel_grid, inital_contour, window_size, movement_threshold):
    # window_size is the length of the side of the square window checked around each contour point
    # movement_threshold is the max movement to be satisfied with
    gradient = find_gradient(pixel_grid)

    movement = movement_threshold + 1
    contour = inital_contour
    while movement > movement_threshold:
        contour = uniformly_sample_contour(contour)
        new_contour = np.array(contour.shape)

        for i in range(len(contour)):
            new_contour[i] = find_next_point(contour[i], gradient, window_size)
    
    return new_contour