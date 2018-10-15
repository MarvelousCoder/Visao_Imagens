""" 
Nome: Raphael Soares Ramos
Matrícula: 140160299

Leia o read_me.txt para mais informações.
"""

import argparse
import cv2 as cv
import numpy as np
from convert import *
from notch_filter import notch_reject_filter
from requirement_2 import locate_airplanes
import glob

def take_pixel(img, i, j):
    pixels = []
    pixels.append(img[i - 1, j + 1])
    pixels.append(img[i, j + 1])
    pixels.append(img[i + 1, j + 1])
    pixels.append(img[i - 1, j])
    pixels.append(img[i, j])
    pixels.append(img[i + 1, j])
    pixels.append(img[i - 1, j - 1])
    pixels.append(img[i, j - 1])
    pixels.append(img[i + 1, j - 1])

    return pixels

def filtro_mediana(img, w, h):
    for i in range(1, h):
        for j in range(1, w):
            lista_filtro = take_pixel(img, i, j)
            lista_filtro.sort()
            img[i, j] = lista_filtro[4]
    return img


def main():
    image_list = [cv.imread(file) for file in glob.glob("Images/*.bmp")]

    height, width, channels = image_list[0].shape
    imagem_media = np.zeros((height, width), dtype = np.uint16)
    for img in image_list:
        aux = rgb_to_ycbcr(img)
        imagem_media += aux[:, :, 0]
    
    imagem_media = imagem_media / len(image_list)
    cv.imwrite("media.bmp", imagem_media)
    aux_image = image_list[0]
    aux_image[:, :, 0] = np.copy(imagem_media)

    imagem_bordada = np.full((height+2, width+2), 255, dtype = np.uint8)
    imagem_bordada[1:-1, 1:-1] = aux_image[:, :, 2]

    imagem_bordada = filtro_mediana(imagem_bordada, width, height)

    imagem_mediana = imagem_bordada[1:-1, 1:-1]
    cv.imwrite("median_image.bmp", imagem_mediana)
    aux_image[:, :, 2] = np.copy(imagem_mediana)

    # Utilizo a transformada de Fourier na componente Cb da Imagem Atual #
    fourier_image = np.fft.fft2(aux_image[:, :, 1])
    fourier_image_shift = np.fft.fftshift(fourier_image)
    # Espectro de Magnitude da componente Cb #
    magnitude_spectrum = 20 * np.log(np.abs(fourier_image_shift))
    cv.imwrite("magnitude_spectrum.bmp", magnitude_spectrum)
    # Realizo a filtragem Notch #
    h_final = notch_reject_filter(fourier_image_shift, 3)
    temp = fourier_image_shift * h_final

    # Transformo a imagem de volta para o domínio do espaço #
    unshifted_temp = np.fft.ifftshift(temp)
    back_image = np.fft.ifft2(unshifted_temp)
    back_image = np.int8(np.abs(back_image))

    # Segunda passada do filtro da Mediana #
    imagem_bordada[1:-1, 1:-1] = np.copy(back_image)
    imagem_bordada = filtro_mediana(imagem_bordada, width, height)
    aux_image[:, :, 1] = imagem_bordada[1:-1, 1:-1]

    # Converto para RGB novamente #
    ycbcr_to_rgb(aux_image)
    cv.imwrite("final_image.bmp", aux_image)
    rgb_to_ycbcr(aux_image)
    locate_airplanes(aux_image)

if __name__ == "__main__":
    main()