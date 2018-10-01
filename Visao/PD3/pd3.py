""" 
Nome: Raphael Soares Ramos
Matrícula: 140160299

Leia o read_me.txt para mais informações.
"""

import argparse
import cv2 as cv
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
    
   
