import numpy as np

def pad(M, padd_width, mode='fill_neighbour', axis=[0,1]):
    r, c = M.shape    

    if isinstance(padd_width, list):
        padd_width_r = padd_width['r']
        padd_width_c = padd_width['c']
    else:
        padd_width_r = padd_width
        padd_width_c = padd_width

    if 0 in axis: 
        M_bar_r = r + padd_width_r  * 2
    else: 
        padd_width_r = 0
        M_bar_r = r

    if 1 in axis:
        M_bar_c = c + padd_width_c  * 2
    else:
        padd_width_c = 0
        M_bar_c = c
        
    M_bar = np.zeros((M_bar_r, M_bar_c))
    r_bar, c_bar = M_bar.shape

    # print(M_bar.shape, r, c, padd_width_r, padd_width_c, M_bar)
    
    for i in range(r):
        for j in range(c):
            M_bar[i + padd_width_r, j + padd_width_c] = M[i, j]


    if 0 in axis: 
        for i in reversed(range(padd_width_r)):
            for j in range(c):
                offset = j + padd_width_c
                # print(i , offset, " : ", M_bar[i, offset], M_bar[i, offset])
                M_bar[i, offset] = M_bar[i + 1, offset]


        for i in range(padd_width_r):
            i_offset = i + r + padd_width_r
            for j in range(c):
                j_offset = j + padd_width_c
                # print(i_offset , j_offset, " : ", M_bar[i_offset, j_offset], M_bar[i_offset - 1, j_offset])
                M_bar[i_offset, j_offset] = M_bar[i_offset - 1, j_offset]

    if 1 in axis:
        for i in reversed(range(padd_width_c)):
            for j in range(r):
                # print(i , j , " : ", M_bar[j, i], M_bar[j , i + 1 ])
                M_bar[j, i] = M_bar[j , i + 1 ]
    
        for i in range(padd_width_c):
            i_offset = i + c + padd_width_c
            for j in range(r):
                # print(i_offset , j , " : ", M_bar[j, i_offset], M_bar[j , i_offset - 1 ])
                M_bar[j, i_offset] = M_bar[j , i_offset - 1 ]

    return M_bar



def konv(I, M, padding_mode='zeros', mode="full"):

    # M = np.flip(M)
    r, c = I.shape
    mr, mc = M.shape
    padd_width_r = mr // 2
    padd_width_c = mc // 2
    
    if mode == "full":
        result = np.zeros((r , c ))
        if mr != mc: 
            width = padd_width_r if padd_width_r > padd_width_c else padd_width_c 
            axis = [0] if padd_width_r > padd_width_c else [1]
            I_pad = pad(I, width, axis=axis)
        else: 
            I_pad = pad(I, padd_width_r)
        loop_r = r
        loop_c = c    

    if mode == "valid":
        result = np.zeros((r - padd_width_r * 2, c - padd_width_c * 2))
        I_pad = I
        loop_r = r - padd_width_r * 2
        loop_c = c - padd_width_c * 2
        
    for i in range(loop_r):
        for j in range(loop_c):
            
            sum = 0
            center_i = i + padd_width_r
            center_j = j + padd_width_c
            
            for k in range(mr):
                for l in range(mc):
                    
                    patch_i = center_i - padd_width_r
                    patch_j = center_j - padd_width_c                  
                    sum = sum + (M[k, l] * I_pad[patch_i + k , patch_j + l])
            
            result[i, j] = sum

    min = np.min(result)
    max = np.max(result)

    return (result - min) * 255 / (max - min)


def gaussian(dimensions, sd):
    G = np.zeros((dimensions,dimensions))
    r, c = G.shape
    middle = dimensions // 2
    for i in range(r):
        for j in range(c):
            x = i - middle
            y = j - middle
            G[i,j] = (1 / (2 * 3.14 * sd**2)) * np.exp(-((x**2 + y**2 ) / (2 * sd**2)))
    return G
    