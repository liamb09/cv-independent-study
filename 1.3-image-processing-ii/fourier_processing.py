from PIL import Image
import numpy as np
import sys
import math
import cmath
import scipy.fft as fft

def intensity (pixel):
    return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]

def to_freq_domain (pixel_grid, p, q):
    sum = 0
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            sum += intensity(pixel_grid[p, q]) * cmath.exp(-2*math.pi*p*row/len(pixel_grid)*1j) * cmath.exp(-2*math.pi*q*col/len(pixel_grid[0])*1j)
    return sum

def hann (pixel_grid):
    h, w, _ = pixel_grid.shape
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[row])):
            pixel_grid[row, col] = pixel_grid[row, col] * (math.sin(math.pi*row/h)**2) * (math.sin(math.pi*col/w)**2)
    return pixel_grid


def convolution_via_fourier (pixel_grid, kernel):
    pass

if len(sys.argv) > 3:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
    inv_dest_path = sys.argv[3]
else:
    sys.exit("Please add command line arguments for source, fft destination, and inv_ftt destination image paths.")

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

# pixel_grid = hann(pixel_grid)

# pixel_grid = []
# for i in range(300):
#     pixel_grid.append([])
#     for j in range(300):
#         if 145 <= i <= 155 and 145 <= j <= 155:
#             pixel_grid[-1].append([255, 255, 255])
#         else:
#             pixel_grid[-1].append([0, 0, 0])
# pixel_grid = np.array(pixel_grid)

# print(pixel_grid)

new_grid = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1]))
for row in range(len(pixel_grid)):
    for col in range(len(pixel_grid[row])):
        new_grid[row, col] = intensity(pixel_grid[row, col])

new_grid = fft.fft2(new_grid)
new_grid = fft.fftshift(new_grid)

row_center = len(new_grid)//2
col_center = len(new_grid[0])//2
for row in range(len(new_grid)):
    for col in range(len(new_grid[row])):
        if math.sqrt((row - row_center)**2 + (col - col_center)**2) > 50:
            new_grid[row, col] = 0

display_new_grid = np.abs(new_grid)
display_new_grid = np.log(1 + display_new_grid)
display_new_grid = (display_new_grid - np.min(display_new_grid)) / (np.max(display_new_grid) - np.min(display_new_grid))*255
print(np.max(display_new_grid))

inv_new_grid = fft.ifftshift(new_grid)
inv_new_grid = fft.ifft2(inv_new_grid)
display_inv_new_grid = np.real(inv_new_grid)

# print(to_freq_domain(pixel_grid, 10, 10))

newimg = Image.fromarray(display_new_grid.astype(np.uint8))
newimg.save(dest_path)

newimg = Image.fromarray(display_inv_new_grid.astype(np.uint8))
newimg.save(inv_dest_path)