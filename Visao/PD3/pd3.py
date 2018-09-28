""" 
Nome: Raphael Soares Ramos
Matrícula: 140160299

Leia o read_me.txt para mais informações.
"""

import argparse
import cv2 as cv
from sklearn.preprocessing import normalize
import numpy as np

def main():
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-w", "--block", required = True, help= "Tamanho do bloco w")
    # # ap.add_argument("-i2", "--image2", required = True, help = "Path para a imagem 2")
    # args = vars(ap.parse_args())

    image_al = cv.imread("data/aloeL.png")
    image_ar = cv.imread("data/aloeR.png")
    image_bl = cv.imread("data/babyL.png")
    image_br = cv.imread("data/babyR.png")
    # SGBM Parameters -----------------
    window_size = 3                     # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
    
    left_matcher = cv.StereoSGBM_create(
        minDisparity=0,
        numDisparities=160,             # max_disp has to be dividable by 16 f. E. HH 192, 256
        blockSize=5,
        P1=8 * 3 * window_size ** 2,    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv.STEREO_SGBM_MODE_SGBM_3WAY
    )
    right_matcher = cv.ximgproc.createRightMatcher(left_matcher)
    # FILTER Parameters
    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0
    
    wls_filter = cv.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    displ = left_matcher.compute(image_al, image_ar)  # .astype(np.float32)/16
    dispr = right_matcher.compute(image_ar, image_al)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)
    filteredImg = wls_filter.filter(displ, image_al, None, dispr)  # important to put "imgL" here!!!
    
    filteredImg = cv.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv.NORM_MINMAX);
    filteredImg = np.uint8(filteredImg)
    cv.imshow('Disparity Map', filteredImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
