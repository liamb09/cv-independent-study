import numpy as np
from PIL import Image
import math

img = Image.open("wrench.jpg")
pixel_grid = np.array(img)

print("Array Shape (Height, Width, Channels):", pixel_grid.shape)
height, width, _ = pixel_grid.shape

area = 0
maxnorm = 0
for i in range(height):
    for j in range(width):
        maxnorm = max(maxnorm, np.linalg.norm(pixel_grid[i, j]))
        if np.linalg.norm(pixel_grid[i, j]) < 415:
            pixel_grid[i, j] = [255, 255, 255]
            area += 1
        else:
            pixel_grid[i, j] = [0, 0, 0]
print(area / (height*width))

com_x = 0
com_y = 0
for i in range(height):
    for j in range(width):
        if np.any(pixel_grid[i, j]):
            com_x += i
            com_y += j
com_x /= area
com_y /= area
print(int(com_x), int(com_y))

for i in range(height):
    for j in range(width):
        if math.sqrt((i-com_x)**2 + (j-com_y)**2) < 3:
            pixel_grid[i, j] = (255, 0, 0)

pixel_grid[int(com_x), int(com_y)] = [255, 0, 0]

newimg = Image.fromarray(pixel_grid)
newimg.save("binary_image.png")

# print("Top-left pixel RGB values:", pixel_grid[0, 0])
# print("Top-left 5x5 pixel block:\n", pixel_grid[0:5, 0:5])