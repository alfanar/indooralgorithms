import numpy as np

def covariance_vector(x, mx, y, my, n):
    s_x = x
    s_y = y
    for i in range(1, 2 * n):
        s_x.T[i] = s_x.T[i] - mx
        s_y.T[i] = s_y.T[i] - my
    c = np.dot(s_x, s_y.T) / (2 * n)
    return c
