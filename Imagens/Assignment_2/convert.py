import cv2 as cv
import numpy as np

""" 
Scale de 128 usado conforme a OpenCV utiliza:
https://docs.opencv.org/3.4.2/de/d25/imgproc_color_conversions.html#color_convert_rgb_ycrcb
"""


def rgb_to_ycbcr(img):
    height, width, channels = img.shape

    Y = np.zeros((height, width), dtype=np.int8)
    Cb = np.zeros((height, width), dtype=np.int8)
    Cr = np.zeros((height, width), dtype=np.int8)

    Y = (0.114 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.299 * img[:, :, 2])
    Cr = (0.713 * img[:, :, 2] - 0.713 * Y + 128)
    Cb = (0.564 * img[:, :, 0] - 0.564 * Y + 128)

    img[:, :, 0] = Y
    img[:, :, 1] = Cr
    img[:, :, 2] = Cb
    return img

def ycbcr_to_rgb(img):
    height, width, channels = img.shape

    R = np.zeros((height, width), dtype=np.int8)
    G = np.zeros((height, width), dtype=np.int8)
    B = np.zeros((height, width), dtype=np.int8)

    R = img[:, :, 0] + (1.403 * img[:, :, 1] - 1.403 * 128)
    G = img[:, :, 0] + (-0.714 * img[:, :, 1] + 0.714 * 128) + (-0.344 * img[:, :, 2] + 0.344 * 128)
    B = img[:, :, 0] + (1.773 * img[:, :, 2] - 1.773 * 128)

    img[:, :, 0] = B
    img[:, :, 1] = G
    img[:, :, 2] = R
    return img
