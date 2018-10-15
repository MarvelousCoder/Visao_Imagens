import numpy as np
import cv2 as cv
from skimage.exposure import rescale_intensity

def convolve(image, kernel, di, dt):
    # grab the spatial dimensions of the image, along with
    # the spatial dimensions of the kernel
    (ih, iw) = image.shape[:2]
    (kh, kw) = kernel.shape[:2]

    # allocate memory for the output image, taking care to
    # "pad" the borders of the input image so the spatial
    # size (i.e., width and height) are not reduced
    pad_w = (kw - 1) // 2
    pad_h = (kh - 1) // 2
    # image = np.zeros((ih+pad_h+2, iw+pad_w+2), dtype = np.uint8)
    image = cv.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv.BORDER_REPLICATE)
    # image[1:(width+1), 1:(height+1)] = img[0:width, 0:height]
    output = np.zeros((ih, iw), dtype="float32")

    # loop over the input image, "sliding" the kernel across
    # each (x, y)-coordinate from left-to-right and top to
    # bottom
    for y in np.arange(pad_h, ih + pad_h):
        for x in np.arange(pad_w, iw + pad_w):
            # extract the ROI of the image by extracting the
            # *center* region of the current (x, y)-coordinates
            # dimensions
            roi = image[y - pad_h:y + pad_h + 1, x - pad_w:x + pad_w + 1]

            # perform the actual convolution by taking the
            # element-wise multiplicate between the ROI and
            # the kernel, then summing the matrix
            k = (roi * kernel).sum()

            # store the convolved value in the output (x,y)-
            # coordinate of the output image
            output[y - pad_h, x - pad_w] = k/(di*dt)
    # return the output image
    return output

def standard_deviation(img, template, nx, ny, avg):
    height, width, channels = img.shape
    
    soma = 0.0
    for y in range(height):
        for x in range(width):
            soma += (img[y,x,0]**2)/(nx*ny) - (img[y,x,0]/(nx*ny))**2

    soma_t = 0.0
    
    for j in range(ny):
        for i in range(nx):
            soma_t += ((template[j, i] - avg)**2)/(nx * ny)


    return np.sqrt(nx*ny) * np.sqrt(soma), np.sqrt(nx*ny) * np.sqrt(soma_t)


def locate_airplanes(img):
    height, width, channels = img.shape
    print("%d %d"%(height, width))

    template = img[549:664, 312:389, 0]
    cv.imwrite("template.bmp", template)
    height_crop, width_crop = template.shape
    print("%d %d"%(height_crop, width_crop))
    pad_template = np.zeros((height, width), dtype = np.uint8)
    pad_template[549:664, 312:389] = template

    # cv.namedWindow("template", cv.WINDOW_NORMAL)
    # cv.imshow("template", pad_template)
    # cv.waitKey(0)
    soma = float(np.sum(template))
    average = soma / (height_crop * width_crop)
    di, dt = standard_deviation(img, template, width_crop, height_crop, average)

    corr = np.zeros((height-height_crop, width-width_crop), dtype = np.float32)
    img = convolve(img[:, :, 0], template, di, dt)
    print(np.amax(img))
    print(np.amin(img))
    # cv.imshow("img", img)
    # cv.waitKey(0)
    # num = numerator(img, pad_template, average, 1, 1, height, width)
    # print(num/(di*dt))
    # for y in range(height - height_crop):
    #     for x in range(width - width_crop):
    #         num = numerator(img, pad_template, average, y, x, height, width)
    #         corr[y, x] = num/(di*dt)
    