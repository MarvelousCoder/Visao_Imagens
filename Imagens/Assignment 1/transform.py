import cv2
import numpy as np

""" 
Fazemos as contas de acordo com os valores disponibilizado no slide 148 do Topic 02.
Pude observar que há uma diferença entre a imagem obtida por mim usando esses valores, e a imagem obtida
usando a função cv2.Color. Isso se deve ao fato de da função cv2.Color usar um fator delta para
transformação:(https://docs.opencv.org/3.4.2/de/d25/imgproc_color_conversions.html#color_convert_rgb_ycrcb).

A função cv2.convertScaleAbs é usada para converter para a escala de unsigned int 8. Como é feito
cálculos com floats, precisamos desta função.

A função cv2.split() é usada para separar os 3 canais da imagem (Blue, Green e Red).
"""

def trans_gray(image):
    (B, G, R) = cv2.split(image)

    Y = 0.299*R + 0.587*G + 0.114*B
    Cr = 0.713*(R-Y)
    Cb = 0.564*(B-Y)
    Y = cv2.convertScaleAbs(Y)
    Cb = cv2.convertScaleAbs(Cb)
    Cr = cv2.convertScaleAbs(Cr)
    
    cv2.namedWindow("Y/Cb/Cr", cv2.WINDOW_NORMAL)
    cv2.imshow("Y/Cb/Cr", np.hstack([Y,Cb, Cr]))
    cv2.waitKey(0)
    
    # trans = cv2.merge([Y, Cr, Cb])
    cv2.imshow("Grey", Y)
    cv2.waitKey(0)
    return Y