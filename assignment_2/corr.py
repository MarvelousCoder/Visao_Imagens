import numpy as np
from scipy.signal import fftconvolve
import cv2 as cv

def main():
    template = cv.imread("template.bmp", 0)
    img = cv.imread("final_image.bmp", 0)

    # final = normxcorr2(template, img, "full")
    # final = final.astype(np.uint8)
    # cv.imshow("final", final)
    # cv.waitKey(0)

    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    print(np.amax(res))
    print(np.amin(res))
    cv.imshow("res", res)
    cv.waitKey(0)
    threshold = 0.4
    h, w = template.shape
    loc = np.where(res >= threshold)
    img_out = np.copy(img)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_out, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    cv.imshow("out", img_out)
    cv.waitKey(0)

    M = cv.getRotationMatrix2D((w/2,h/2),-18,1)
    dst = cv.warpAffine(template, M, (w, h))
    res = cv.matchTemplate(img, dst, cv.TM_CCOEFF_NORMED)
    w, h = dst.shape[::-1]
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    cv.imshow("out", img)
    cv.waitKey(0)


if __name__ == '__main__':
    main()