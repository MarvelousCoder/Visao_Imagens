import numpy as np

def notch_pair(img, num_pairs, d_zero, uK, vK):
    height, width = img.shape
    # Crio duas matrizes para o Notch H+ e H- #
    h_plus  = np.ones((height, width), dtype=np.float16)
    h_minus = np.ones((height, width), dtype=np.float16)
    # Defino o centro #
    center = (height/2, width/2)
    # Para cada pixel aplico a equação de Notch ButterWorth #
    for i in range(height):
        for j in range(width):
            d_plus  = np.sqrt( (i - center[0] - uK)**2 + (j - center[1] - vK)**2)
            d_minus = np.sqrt( (i - center[0] + uK)**2 + (j - center[1] + vK)**2)

            h_plus[i, j]   = 1/(1 + (d_zero/d_plus)**(2*num_pairs))
            h_minus[i, j]  = 1/(1 + (d_zero/d_minus)**(2*num_pairs))

    return h_minus * h_plus

def notch_reject_filter(img, num_pairs):
    # Função para chamar os pares
    h_final = notch_pair(img, num_pairs, 15, 73.29, 73.528)
    h_final = h_final * notch_pair(img, num_pairs, 15, -73.29, 73.528)
    h_final = h_final * notch_pair(img, num_pairs, 5, 218.844, 73.528)
    h_final = h_final * notch_pair(img, num_pairs, 5, -218.844, 73.528)
    h_final = h_final * notch_pair(img, num_pairs, 5, 72.719, 219.47)
    h_final = h_final * notch_pair(img, num_pairs, 5, -72.719, 219.47)

    return h_final
