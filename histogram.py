import numpy as np

def threshold_binary(I, threshold_value):
    h, w = I.shape

    I_bar = np.zeros((h,w), dtype=np.uint8)

    for i in range(h):
        for j in range(w):            
            if I[i,j] > threshold_value:                
                I_bar[i,j] = 1

    return I_bar
    
def threshold_intensity(I, threshold_value, invert=False):
    h, w = I.shape

    I_bar = np.zeros((h,w), dtype=np.uint8)

    for i in range(h):
        for j in range(w):   
            if invert:
                if I[i,j] <= threshold_value:                
                    I_bar[i,j] = I[i,j]
            else:
                if I[i,j] > threshold_value:                
                    I_bar[i,j] = I[i,j]

    return I_bar


def threshold(I, threshold_value, mode):

    if mode == "BINARY":
        return threshold_binary(I, threshold_value)
    
    if mode == "TOZERO":
        return threshold_intensity(I, threshold_value)
    
    if mode == "TOZERO_INV":
        return threshold_intensity(I, threshold_value, invert=True)
    
    return I

