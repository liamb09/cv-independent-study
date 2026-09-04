import numpy as np
import math
from binary_img_utils import Binary_Image

binary_image = Binary_Image("images/spatula.jpg")
binary_image.to_binary(80)

area = binary_image.area()
print("Area:", area)

com_x, com_y = binary_image.com()
print(com_x, com_y)

binary_image.add_dot(com_x, com_y)

binary_image.second_moments()

binary_image.write_image("binary_image.png")