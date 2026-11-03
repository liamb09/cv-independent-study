import curve_fitting
import math
import sys
from PIL import Image
import numpy as np
import active_contours
import hough_transform

if len(sys.argv) > 2:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
elif len(sys.argv) > 1:
    src_path = sys.argv[1]
    dest_path = "gradient.jpg"
else:
    sys.exit("Please add command line arguments for source and destination image paths.")

# test_points = [(0, 9.38), (1, 12.08), (2, 12.89), (3, 22.02), (4, 22.45), (5, 20.33), (6, 29.09), (7, 28.88), (8, 35.66), (9, 35.66), (10, 38.11), (11, 39.2), (12, 38.3), (13, 42.69), (14, 46.48), (15, 50.45), (16, 40.56), (17, 42.1), (18, 43.45), (19, 51.86), (20, 50.05), (21, 48.19), (22, 55.22), (23, 48.8), (24, 52.81), (25, 48.72), (26, 56.0), (27, 51.5), (28, 55.74), (29, 55.48), (30, 51.55), (31, 52.46), (32, 56.13), (33, 49.89), (34, 53.82), (35, 53.1), (36, 50.2), (37, 47.23), (38, 50.63), (39, 49.13), (40, 50.34), (41, 50.6), (42, 42.8), (43, 49.48), (44, 45.99), (45, 51.58), (46, 49.62), (47, 44.65), (48, 44.71), (49, 50.32), (50, 49.34), (51, 44.35), (52, 41.82), (53, 45.27), (54, 45.5), (55, 43.28), (56, 46.83), (57, 52.6), (58, 50.52), (59, 44.35), (60, 50.6), (61, 50.28), (62, 52.34), (63, 57.56), (64, 50.63), (65, 55.73), (66, 59.42), (67, 60.12), (68, 56.21), (69, 63.68), (70, 63.27), (71, 63.09), (72, 68.88), (73, 74.83), (74, 78.59), (75, 79.2), (76, 80.89), (77, 80.41), (78, 83.82), (79, 89.71), (80, 94.23), (81, 93.07), (82, 100.31), (83, 108.65), (84, 108.02), (85, 118.21), (86, 118.45), (87, 127.46), (88, 129.28), (89, 137.15), (90, 139.63), (91, 150.75), (92, 160.36), (93, 161.79), (94, 172.06), (95, 174.91), (96, 185.31), (97, 187.69), (98, 202.29), (99, 213.57)]
# polynomial_coefficients = curve_fitting.fit_polynomial(test_points, 3)
# print(polynomial_coefficients)
# print(" + ".join([f"{polynomial_coefficients[i]:.10f}x^{i}" for i in range(len(polynomial_coefficients))]))

# start_contour = [(671,519),(717,405),(708,246),(610,157),(419,133),(311,200),(282,342),(363,500),(570,540)]
# active_contours.uniformly_sample_contour(start_contour)

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

edges = hough_transform.detect_lines(pixel_grid, True)

newimg = Image.fromarray(edges.astype(np.uint8))
newimg.save(dest_path)