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

def trans_gray_eq(image):
    (B, G, R) = cv2.split(image)

    Y = 0.299*R + 0.587*G + 0.114*B
    Cr = 0.713*(R-Y) + 128
    Cb = 0.564*(B-Y) + 128
    Y = cv2.convertScaleAbs(Y)
    Cb = cv2.convertScaleAbs(Cb)
    Cr = cv2.convertScaleAbs(Cr)
    
    cv2.namedWindow("Y/Cb/Cr", cv2.WINDOW_NORMAL)
    cv2.imshow("Y/Cb/Cr", np.hstack([Y,Cb, Cr]))
    cv2.waitKey(0)
    
    # trans = cv2.merge([Y, Cr, Cb])
    return equalizar(Y) # Retornamos a imagem cinza equalizada 

def equalizar(img):
    width = img.shape[1] 
    height = img.shape[0] 
    menor_intensidade = np.amin(img) # Pego o valor do pixel mais escuro da imagem
    maior_intensidade = np.amax(img) # Pego o valor do pixel mais claro  da imagem
    
    probabilidades = np.zeros(maior_intensidade + 1, dtype = int) 
    """ probabilidades foi criado que o algoritmo rode mais rápido. Ele funciona da seguinte forma:
        - É um numpy array onde todos os elementos iniciam com zero.
        - Cada elemento é a quantidade de vezes que o pixel com aquela intensidade aparece na imagem.
            Por exemplo, se probabilidades[0] = 1, significa que o pixel com intensidade 0 aparece 
            uma vez na imagem.
        - O numpy array possui maior_intensidade + 1 elementos, devido a forma que ele funciona.
        - Note que os elementos dos índices x, tal que x < menor_intensidade terão o valor sempre zero. 
          Entretanto, isso não importa.
    """

   
    for j in range(height): # Percorro a imagem para saber a quant. de pixels em cada tom, o h(r_k)= n_k
        for i in range(width):
            if (probabilidades[img[j, i]] > 0): 
                probabilidades[img[j, i]] += 1
            else:
                probabilidades[img[j, i]] = 1
    """ No primeiro if do for acima verificamos se o pixel x já apareceu antes.
        Se ele já apareceu, incrementamos a quantidade de vezes que ele apareceu.
        Fazemos isso acessando o conteúdo do elemento x do array, que guarda a quantidade de vezes
        que o pixel x aparece na imagem.
    """

    probabilidades = (probabilidades)/(height*width)
     # Calculo a probabilidade de cada pixel na imagem n_k/(quant. pixels)
    
    for i in range(1, maior_intensidade + 1): # Faço soma de prefixos para obter prob. acumulada
        probabilidades[i] += probabilidades[i-1]
    """ Nesse for da da linha 37 é feito soma de prefixos. A soma de prefixos funciona da seguinte forma:
        - O elemento 0 fica com o seu valor original.
        - A partir do elemento 1, somamos o valor do elemento mais o elemento anterior.
        - Assim, elemento 1 = elemento 1 + 0, elemento 2 = elemento 2 + elemento 1 e assim por diante.
    """

    probabilidades = probabilidades*(maior_intensidade-1)
    # Multiplico o valor antigo por (L-1) para obter s_k = T(r_k). Aqui já tenho os somatórios guardados.

    probabilidades = np.around(probabilidades)
    # Arrendondo o valor e obtenho s a ser usado na imagem.
    # Se x = 4.5, então np.around(x) = 4 que é o par mais próximo.

    for j in range(height): # Percorro a imagem para pintá-la
        for i in range(width):
            img[j, i] = probabilidades[img[j, i]] # Substituo o pixel pelo valor de s calculado acima

    cv2.imshow("Imagem Equalizada", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img
