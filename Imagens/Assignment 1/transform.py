import cv2
import numpy as np

def transYcbcr(image):
    (B, G, R) = cv2.split(image)

    Y = 0.299*R + 0.587*G + 0.114*B
    Cb = 0.564*(B-Y)
    Cr = 0.713*(R-Y)
    Y = cv2.convertScaleAbs(Y)
    Cb = cv2.convertScaleAbs(Cb)
    Cr = cv2.convertScaleAbs(Cr)
    
    cv2.namedWindow("Y/Cb/Cr", cv2.WINDOW_NORMAL)
    cv2.imshow("Y/Cb/Cr", np.hstack([Y,Cb, Cr]))
    cv2.waitKey(0)
    
    trans = cv2.merge([Y, Cb, Cr])
    cv2.imshow("YCbCr", trans)
    cv2.waitKey(0)