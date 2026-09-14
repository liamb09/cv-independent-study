import numpy as np
import math
from PIL import Image, ImageDraw
import random

class Binary_Image:
    def __init__(self, path):
        self.img = Image.open(path).convert("RGB")
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
    
    def draw_fullscreen_line(self, draw, p1, p2):
        # numpy array and ImageDraw use inverted dimension ordering
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
        # draw = ImageDraw.Draw(newimg)
        # self.draw_fullscreen_line(draw, (com_x, com_y), (com_x+100, com_y + (100)*math.tan(self.orientation)))
        newimg.save(new_name)
    
    def sample_area (self, segmented_grid, row, col):
        # left, topleft, top
        l = tl = t = 0
        if row == 0:
            if col != 0:
                l = segmented_grid[-1][-1]
        else:
            t = segmented_grid[-2][col]
            # self.pixel_grid(row-1, col)
            if col != 0:
                l = segmented_grid[-1][-1]
                # self.pixel_grid(row, col-1)
                tl = segmented_grid[-2][col-1]
                # self.pixel_grid(row-1, col-1)
        return l, tl, t
    
    def find_root (self, equivalence_table, key, in_recursion=False):
        val = equivalence_table[key]
        if len(val) == 0:
            if not in_recursion:
                return []
            else:
                return [key]
        else:
            root = self.find_root(equivalence_table, val[0], True)
            for i in val[1:]:
                equivalence_table[i] = root
            return root

    # def segment (self):
    #     segmented_grid = []
    #     equivalence_table = {}
    #     next_index = 1

    #     # colors = [[230, 25, 75], [60, 180, 75], [255, 225, 25], [0, 130, 200], [245, 130, 48], [145, 30, 180], [70, 240, 240], [240, 50, 230], [210, 245, 60], [250, 190, 212], [0, 128, 128], [220, 190, 255], [170, 110, 40], [255, 250, 200], [128, 0, 0], [170, 255, 195], [128, 128, 0], [255, 215, 180], [0, 0, 128], [128, 128, 128], [255, 255, 255]]
    #     for i in range(self.height):
    #         segmented_grid.append([])
    #         for j in range(self.width):
    #             # if background
    #             if not np.any(self.pixel_grid[i, j]):
    #                 segmented_grid[-1].append(0)
    #             else:
    #                 l, tl, t = self.sample_area(segmented_grid, i, j)
    #                 if l == tl == t == 0:
    #                     equivalence_table[next_index] = []
    #                     segmented_grid[-1].append(next_index)
    #                     next_index += 1
    #                 elif tl != 0:
    #                     segmented_grid[-1].append(tl)
    #                 elif tl == t == 0 and l != 0:
    #                     segmented_grid[-1].append(l)
    #                 elif tl == l == 0 and t != 0:
    #                     segmented_grid[-1].append(t)
    #                 elif l != 0 and t != 0:
    #                     if t != l:
    #                         # if equivalence_table[min(l,t)] == []:
    #                         equivalence_table[max(l,t)].append(min(l,t))
    #                         # else:
    #                             # equivalence_table[max(l,t)] = equivalence_table[min(l,t)]
    #                     segmented_grid[-1].append(l)
    #     # print(len(equivalence_table))
        
    #     print(equivalence_table)
    #     for [key, val] in equivalence_table.items():
    #         equivalence_table[key] = self.find_root(equivalence_table, key)
    #     print(equivalence_table)

    #     for [key, val] in equivalence_table.items():
    #         if val == []:
    #             print(key)

    #     # for i in range(self.height):
    #     #     # if len(segmented_grid[i]) != 500:
    #     #     #     print(segmented_grid[i])
    #     #     for j in range(self.width):
    #     #         if segmented_grid[i][j] != 0:
    #     #             segmented_grid[i][j] = colors[uniques.index(equivalence_table[segmented_grid[i][j]][0])]
    #     #         else:
    #     #             segmented_grid[i][j] = [0, 0, 0]


    #     # newarr = np.array(segmented_grid, dtype=np.uint8)
    #     # newimg = Image.fromarray(newarr)
    #     # newimg.save("segmented.bmp")

    def segment (self):
        segmented_grid = []
        equivalence_table = {}
        next_index = 1

        colors = [[230, 25, 75], [60, 180, 75], [255, 225, 25], [0, 130, 200], [245, 130, 48], [145, 30, 180], [70, 240, 240], [240, 50, 230], [210, 245, 60], [250, 190, 212], [0, 128, 128], [220, 190, 255], [170, 110, 40], [255, 250, 200], [128, 0, 0], [170, 255, 195], [128, 128, 0], [255, 215, 180], [0, 0, 128], [128, 128, 128], [255, 255, 255]]
        for i in range(self.height):
            segmented_grid.append([])
            for j in range(self.width):
                # if background
                if not np.any(self.pixel_grid[i, j]):
                    segmented_grid[-1].append(0)
                else:
                    l, tl, t = self.sample_area(segmented_grid, i, j)
                    if l == tl == t == 0:
                        equivalence_table[next_index] = []
                        segmented_grid[-1].append(next_index)
                        next_index += 1
                    elif tl != 0:
                        segmented_grid[-1].append(tl)
                    elif tl == t == 0 and l != 0:
                        segmented_grid[-1].append(l)
                    elif tl == l == 0 and t != 0:
                        segmented_grid[-1].append(t)
                    elif l != 0 and t != 0:
                        if t != l:
                            equivalence_table[l].append(t)
                        segmented_grid[-1].append(l)

        print(list(equivalence_table.items())[0:3])
        for [key, val] in equivalence_table.items():
            print(key, end=" ")
            equivalence_table[key] = [self.find_root(equivalence_table, key)]
            print(equivalence_table[key])

        uniques = []
        for [key, val] in equivalence_table.items():
            if val[0] not in uniques:
                uniques.append(val[0])
        print(uniques, len(uniques))

        colors = [[
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        ] for _ in range(len(uniques))]

        for i in range(self.height):
            # if len(segmented_grid[i]) != 500:
            #     print(segmented_grid[i])
            for j in range(self.width):
                if segmented_grid[i][j] != 0:
                    segmented_grid[i][j] = colors[uniques.index(equivalence_table[segmented_grid[i][j]][0])]
                else:
                    segmented_grid[i][j] = [0, 0, 0]
    
        # print(equivalence_table)

        newarr = np.array(segmented_grid, dtype=np.uint8)
        newimg = Image.fromarray(newarr)
        newimg.save("segmented.bmp")