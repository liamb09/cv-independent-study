import numpy as np
import cv2
import math

sobel = (
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

def to_greyscale (pixel_grid):
    new_grid = []

    for row in pixel_grid:
        new_grid.append([])
        for pixel in row:
            new_grid[-1].append(0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2])

    return np.array(new_grid)

def gaussian (pixel_grid, sigma):
    kernel_size = 2 * math.ceil(3*sigma) + 1
    variance = sigma ** 2

    hor_kernel = np.array([[0 for i in range(kernel_size)]]).astype(float)
    ver_kernel = np.array([[0] for i in range(kernel_size)]).astype(float)

    for i in range(kernel_size):
        val = math.e ** (-0.5 * ((i - math.floor(kernel_size/2))**2) / variance)
        hor_kernel[0][i] = val / (2 * math.pi * variance)
        ver_kernel[i][0] = val

    # print(hor_kernel, "\n", ver_kernel)
    
    blurred = cv2.filter2D(pixel_grid, -1, hor_kernel)
    blurred = cv2.filter2D(blurred, -1, ver_kernel)

    return blurred

def canny_ed (pixel_grid, sigma):
    pixel_grid = to_greyscale(pixel_grid)
    smoothed = gaussian(pixel_grid, sigma)

    gradient_x = cv2.filter2D(smoothed, -1, sobel[0])
    gradient_y = cv2.filter2D(smoothed, -1, sobel[1])

    # magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

    # display_image = cv2.normalize(
    #     magnitude, None, 0, 255, cv2.NORM_MINMAX
    # ).astype(np.uint8)

    # in multivariable calculus, derivative of a scalar-valued function f at P in the
    #   direction of m is equal to ∇f(P) * m/||m||. Here, ∇f = m = (I_x, I_y), where
    #   I_x and I_y are the partial derivatives of the image in the x and y direction
    #   respectively. Therefore the laplacian along the gradient here is equal to
    #   (I_x^2 + 2*I_x*I_y + I_y^2)/(I_x^2+I_y^2)
    
    gradient_laplacian = [] # the laplacians at each point in the gradient direction
    for row in range(len(gradient_x)):
        gradient_laplacian.append([])
        for col in range(len(gradient_x[0])):
            # gradient_mag = math.sqrt(
            #     gradient_x[row][col]**2 + gradient_y[row][col]**2
            # )
            # gradient_orientation = math.atan(
            #     gradient_y[row][col] / gradient_x[row][col]
            # )

            gradient_laplacian[-1].append(
                (
                    gradient_x[row][col]**2 + 
                    2*gradient_x[row][col]*gradient_y[row][col] +
                    gradient_y[row][col]**2
                ) / (gradient_x[row][col]**2 + gradient_y[row][col]**2)
            )
    gradient_laplacian = np.array(gradient_laplacian)
    print(gradient_laplacian)

    return gradient_x