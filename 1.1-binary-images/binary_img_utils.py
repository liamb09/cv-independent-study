import numpy as np
import math
from PIL import Image, ImageDraw

class Binary_Image:
    def __init__(self, path):
        self.img = Image.open(path)
        self.pixel_grid = np.array(self.img)
        self.height, self.width, _ = self.pixel_grid.shape
        self.orientation = None

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
                if math.sqrt((i-x)**2 + (j-y)**2) < 8:
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
        b *= 2

        self.orientation = 0.5*math.atan2(b, a-c)

        self.add_dot(com_x, com_y)

        return a, b, c
    
    def draw_fullscreen_line(self, draw, p1, p2) :
        draw.line([
            (p1[1], p1[0]),
            (p1[1] + (p2[1] - p1[1])*10, p1[0] + (p2[0] - p1[0])*10)
        ], fill="red", width=3)
        draw.line([
            (p1[1], p1[0]),
            (p1[1] - (p2[1] - p1[1])*10, p1[0] - (p2[0] - p1[0])*10)
        ], fill="red", width=3)

    def write_image (self, new_name):
        com_x, com_y = self.com()
        newimg = Image.fromarray(self.pixel_grid)
        draw = ImageDraw.Draw(newimg)
        # numpy array and ImageDraw use inverted dimension ordering
        self.draw_fullscreen_line(draw, (com_x, com_y), (com_x+100, com_y + (100)*math.tan(self.orientation)))
        newimg.save(new_name)