import numpy as np

def color_to_grayscale(I):

    h, w, _ = I.shape

    I_bar = np.zeros((h,w), dtype=np.uint8)

    for i in range(h):
        for j in range(w):

            r, g, b = I[i, j]

            I_bar[i,j] = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return I_bar