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

if len(sys.argv) > 2:
    src_path = sys.argv[1]
    dest_path = sys.argv[2]
else:
    sys.exit("Please add command line arguments for source and destination image paths.")

img = Image.open(src_path).convert("RGB")
pixel_grid = np.array(img)

pixel_grid = hann(pixel_grid)

# pixel_grid = []
# for i in range(300):
#     pixel_grid.append([])
#     for j in range(300):
#         pixel_grid[-1].append([255 * ((1 + math.cos(j))/2) * (1 + math.cos(j/10))/2 * (math.sin(math.pi*i/300)**2) * (math.sin(math.pi*j/300)**2)]*3)
# pixel_grid = np.array(pixel_grid)

# print(pixel_grid)

new_grid = np.zeros((pixel_grid.shape[0], pixel_grid.shape[1]))
for row in range(len(pixel_grid)):
    for col in range(len(pixel_grid[row])):
        new_grid[row, col] = intensity(pixel_grid[row, col])

new_grid = fft.fftshift(fft.fft2(new_grid))
# print(new_grid)
new_grid = np.abs(new_grid)
# print(new_grid)
new_grid = np.log(1 + new_grid)
new_grid = (new_grid - np.min(new_grid)) / (np.max(new_grid) - np.min(new_grid))*255
print(np.max(new_grid))

# print(new_grid[new_grid != 0])

# print(to_freq_domain(pixel_grid, 10, 10))

newimg = Image.fromarray(new_grid.astype(np.uint8))
newimg.save(dest_path)