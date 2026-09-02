import numpy as np
import math
from PIL import Image, ImageDraw

class Binary_Image:
    def __init__(self, path):
        self.img = Image.open("spatula-rotated.jpg")
        self.pixel_grid = np.array(self.img)
        self.height, self.width, _ = self.pixel_grid.shape

    def to_binary (self, greyscale_threshold):
        for i in range(self.height):
            for j in range(self.width):
                gray = 0.299*self.pixel_grid[i, j][0] + 0.587*self.pixel_grid[i, j][1] + 0.114*self.pixel_grid[i, j][2]
                if (gray > greyscale_threshold) if (greyscale_threshold < 128) else (gray < greyscale_threshold):
                    self.pixel_grid[i, j] = [255, 255, 255]
                else:
                    self.pixel_grid[i, j] = [0, 0, 0]
        return self.pixel_grid

    def area (self):
        area = 0
        for i in range(self.height):
            for j in range(self.width):
                if np.any(self.pixel_grid[i, j]):
                    area += 1
        return area

    def first_moment (self, for_x):
        moment = 0
        for i in range(self.height):
            for j in range(self.width):
                if np.any(self.pixel_grid[i, j]):
                    moment += i if for_x else j
        return moment

    def com (self):
        com_x = self.first_moment(True) / self.area()
        com_y = self.first_moment(False) / self.area()
        return com_x, com_y

    def add_dot (self, x, y):
        for i in range(int(x)-5, int(x)+5):
            for j in range(int(y)-5, int(y)+5):
                if math.sqrt((i-x)**2 + (j-y)**2) < 3:
                    self.pixel_grid[i, j] = [255, 0, 0]

    def second_moments (self):
        com_x, com_y = self.com()
        a = b = c = 0
        for i in range(self.height):
            for j in range(self.width):
                if np.any(self.pixel_grid[i, j]):
                    a += (i-com_x)**2
                    b += (i-com_x) * (j-com_y)
                    c += (j-com_y)**2

        theta = math.atan(b/(a-c)) + math.pi/2
        draw = ImageDraw.Draw(self.img)
        draw.line([com_x, com_y, com_x + 100, com_y + (com_x - 100)*math.tan(theta)], fill="red", width=5)
        draw.line([0, 0, 100, 100], fill="red", width=5)

        return a, b, c

    def write_image (self, new_name):
        newimg = Image.fromarray(self.pixel_grid)
        draw = ImageDraw.Draw(newimg)
        draw.line([0, 0, 100, 100], fill="red", width=5)
        newimg.save(new_name)