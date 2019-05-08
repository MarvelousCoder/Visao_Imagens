import numpy as np
import cv2 as cv
from skimage.exposure import rescale_intensity

def convolve(img, kernel, mode):
    # Pego as dimensões espaciais da imagem e do kernel
    ih, iw = img.shape
    kh, kw = kernel.shape

    pad_w = (kw - 1) // 2 # a (slide 86 tópico 3)
    pad_h = (kh - 1) // 2 # b (podemos fazer isso pois kw e kw são ímpares).

    """ 
    Pega a imagem de input e coloca no centro de uma imagem maior que contém as bordas replicadas.
    Isso é necessário devido a forma que a convolução funciona, onde cada pixel da imagem será o centro do kernel
    e terá um valor novo.
    """
    image = cv.copyMakeBorder(img, pad_h, pad_h, pad_w, pad_w, cv.BORDER_REPLICATE)
    # image = cv.copyMakeBorder(img, pad_h, pad_h, pad_w, pad_w, cv.BORDER_CONSTANT, (0,0,0))

    # Crio a imagem de output
    output = np.zeros((ih, iw), dtype= np.float32)
    average_kernel = float(np.sum(kernel)) / (kh*kw)

    # Passamos o kernel da esquerda para a direita e do topo para baixo para cada ponto (x, y) da imagem img
    for y in np.arange(pad_h, ih + pad_h):
        for x in np.arange(pad_w, iw + pad_w):
            """ Extraímos a região de interesse (roi) da imagem, extraindo a região cujo centro 
            é a atual coordenada (x,y). 
            """
            roi = image[y - pad_h:y + pad_h + 1, x - pad_w:x + pad_w + 1]
            soma = float(np.sum(roi))
            average = soma / (roi.shape[0] * roi.shape[1])

            """ 
            - Se mode != "cross" fazemos a convolução do kernel com a imagem fazendo a multiplicação element-wise do ROI
            e do kernel, e então somando todos os elementos da matriz.
            - Se mode == "cross" calculamos o numerador e denominador conforme a equação de cross-correlação fornecida.
            """
            if(mode == "cross"):
                denominador = ( (kernel-average_kernel)**2 * (roi - average)**2 ).sum()
                numerador = ( (kernel-average_kernel) * (roi - average) ).sum()
                k = numerador/np.sqrt(denominador)
            else:
                k = (kernel * roi).sum()

            # Guardamos o valor convoluído na coordenada (x,y) da imagem de saída (output).
            output[y - pad_h, x - pad_w] = k

    return output


def locate_airplanes(img):
    height, width = img.shape

    template = img[549:664, 312:389]
    height_crop, width_crop = template.shape

    # Rotaciona o template em 180° antes para fazer correlação. Entretanto não faz diferença no resultado obtido.
    # M = cv.getRotationMatrix2D((width_crop/2,height_crop/2),-180,1) 
    # template = cv.warpAffine(template, M, (width_crop, height_crop))
    template_aux = np.copy(template)

    for i in range(-45,45,9): # Testo os ângulos entre -45 a 45°
        M = cv.getRotationMatrix2D((width_crop/2,height_crop/2),i,1)
        template = cv.warpAffine(template_aux, M, (width_crop, height_crop))
        print("%d graus"%i)
        cv.namedWindow("Template " + str(i) + "°", cv.WINDOW_NORMAL)
        cv.imshow("Template " + str(i) + "°", np.hstack([template_aux, template]))
        cv.waitKey(0)
        print("Calculando cross-correlation...")
        output = convolve(img, template, "cross")
        # teste = (teste - np.amin(teste))/(np.amax(teste) - np.amin(teste))
        # teste = rescale_intensity(teste, in_range=(-1, 1))
        # teste = (teste * 255).astype(np.uint8)

        # Aplico o threshold na imagem para exibir locais da imagem com alta correlação 
        threshold = np.amax(output) - 1.0
        loc = np.where(output >= threshold)
        img_out = np.copy(img)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_out, pt, (pt[0] + width_crop, pt[1] + height_crop), (0,0,255), 2)

        # Exibe a imagem com os retângulos para os "aviões encontrados".
        cv.imshow("Avioes Encontrados", img_out)
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == '__main__':
    img = cv.imread("final_image.bmp", 0)
    locate_airplanes(img)
    