import math

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