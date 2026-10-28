import math
import numpy as np

def fit_line (points):
    com_x = 0
    com_y = 0
    for p in points:
        com_x += p[0]
        com_y += p[1]
    com_x /= len(points)
    com_y /= len(points)

    a = b = c = 0
    for p in points:
        a += (p[0]-com_x)**2
        b += (p[0]-com_x) * (p[1]-com_y)
        c += (p[1]-com_y)**2
    b *= 2

    orientation = 0.5*math.atan2(b, a-c)
    
    return com_x, com_y, orientation

def fit_polynomial (points, degree=3):
    X = [] # matrix of x^n, x^(n-1), ... x^2, x for each x_i in points
    Y = np.array([p[1] for p in points]) # y_i for i in points
    for p in points:
        X.append([p[0]**i for i in range(degree+1)])
    X = np.array(X)

    # compute psuedo inverse of X because X isn't necessarily square
    # X_pinv = np.linalg.pinv(X)
    X_pinv = np.linalg.inv(X.T @ X) @ X.T
    A = X_pinv @ Y # matrix of constants, e.g. the a, b, c, and d in ax^3 + bx^2 + cx + d
    # print(X.shape, X_pinv.shape, Y.shape, A.shape)
    # print(X_pinv)
    # print(Y)

    return A